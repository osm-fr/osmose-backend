import sys
import os
import re
import ast
import hashlib
from pprint import pprint
from antlr4 import *
from generated.MapCSSLexer import MapCSSLexer
from generated.MapCSSParser import MapCSSParser
from MapCSSListenerL import MapCSSListenerL


# Clean

def valueExpression_remove_null_op(t, c):
    """
    type = valueExpression
    Remove useless valueExpression
    """
    if not t['operator'] and len(t['operands']) == 1:
        t = t['operands'][0]
    return t

def primaryExpression_remove_null_op(t, c):
    """
    type = primaryExpression
    Remove useless valueExpression
    """
    if not t['derefered'] and isinstance(t['value'], dict):
        t = t['value']
    return t

def quoted_unescape(t, c):
    """
    type = quoted
    Remove surrounding quotes and unescape content
    """
    if not 'unescape' in t:
        t['unescape'] = True
        t['value'] = ast.literal_eval("u" + t['value'])
    return t

def regexExpression_unescape(t, c):
    """
    type = regexExpression
    Remove surrounding slash and unescape content
    """
    if not 'unescape' in t:
        t['unescape'] = True
        t['value'] = ast.literal_eval("r\"" + t['value'].replace("\\'", "'").replace('\\"', '"').replace('"', '\\"') + "\"")
    return t

def simple_selector_pseudo_class(t, c):
    """
    type = simple_selector
    Remove allways true pseudo class
    """
    t['pseudo_class'] = list(filter(lambda p: not(p['not_class'] and p['pseudo_class'] in ('completely_downloaded', 'in-downloaded-area')), t['pseudo_class']))
    return t

def functionExpression_eval(t, c):
    """
    type = functionExpression
    Remove call to eval
    """
    if t['name'] == 'eval':
        t = t['params'][0]
    return t


# Rewrite

def primary_expression_derefered(t, c):
    """
    type = primaryExpression
    Replace defered operator by a function call
    """
    if t['derefered']:
        t['derefered'] = None
        t = {'type': 'functionExpression', 'name': 'tag', 'params': [t]}
    return t

def predicate_simple_dereference(t, c):
    """
    type = predicate_simple
    Replace predicate by a function call
    """
#    if t['predicate']['type'] != 'functionExpression': # Do only once
    if not t['not']:
        c['selector_capture'].append(t['predicate'])
    t['predicate'] = {'type': 'functionExpression', 'name': '_tag_capture', 'params': [t['predicate']]}
    return t

def booleanExpression_dereference_first_operand(t, c):
    """
    type = booleanExpression
    Replace first operand by the value of the tag
    """
    if len(t['operands']) >= 1 and t['operands'][0]['type'] in ('osmtag', 'quoted'):
        t['operands'][0] = {'type': 'functionExpression', 'name': 'tag', 'params': [t['operands'][0]]}
    return t

def booleanExpression_capture_first_operand(t, c):
    """
    type = booleanExpression
    Capture first operand tag
    """
    if len(t['operands']) >= 1 and t['operands'][0]['type'] == 'functionExpression' and t['operands'][0]['name'] == 'tag':
        if not t['operator'] in ('!', '!=', '!~'):
            c['selector_capture'].append(t['operands'][0]['params'][0])
        t['operands'][0] = {'type': 'functionExpression', 'name': '_tag_capture', 'params': [t['operands'][0]['params'][0]]}
    return t

def booleanExpression_negated_operator(t, c):
    """
    type = booleanExpression
    Replace !~ by !(... =~ ...)
    """
    if t['operator'] == '!~':
        t['operator'] = '=~'
        t = {'type': 'booleanExpression', 'operator': '!', 'operands': [t]}
    return t

booleanExpression_operator_to_function_map = {
    '=~': 'regexp_test',
    '^=': 'startswith', '$=': 'endswith',
    '*=': 'string_contains',
    '~=': 'list_contains',
}

def booleanExpression_operator_to_function(t, c):
    """
    type = booleanExpression
    Replace operator by a function call
    """
    if t['operator'] == '=~':
        t = {'type': 'functionExpression', 'name': booleanExpression_operator_to_function_map[t['operator']], 'params': [
            t['operands'][1],
            t['operands'][0]
        ]}
    elif t['operator'] in booleanExpression_operator_to_function_map.keys():
        # Direct prams order
        t = {'type': 'functionExpression', 'name': booleanExpression_operator_to_function_map[t['operator']], 'params': [
            t['operands'][0],
            t['operands'][1]
        ]}
    return t

def declaration_value_function_param_regex(t, c):
    """
    type = declaration_value_function
    Ensure params to regex functions are regex
    """
    if t['name'] in ('regexp_test', 'regexp_match'):
        if t['params'][0]['type'] == 'single_value' and t['params'][0]['value']['type'] == 'quoted':
            t['params'][0]['value'] = {'type': 'regexExpression', 'value': t['params'][0]['value']['value']}
    return t

rule_declarations_order_map = {
    # subclass
    'group': 1,
     # text
    'throwError': 2,
    'throwWarning': 2,
    'throwOther': 2,
    'suggestAlternative': 2,
    # fix
    'fixAdd': 3,
    'fixChangeKey': 3,
    'fixRemove': 3,
    'fixDeleteObject': 3,
    # test
    'assertMatch': 4,
    'assertNoMatch': 4,
}

def rule_declarations_order(t, c):
    """
    type = rule
    Order the declarations in order attended by the code generator
    """
    t['declarations'] = sorted(t['declarations'], key = lambda d: (d.get('property') and [rule_declarations_order_map.get(d['property']), str(d['value'])]) or [-1, -1])
    return t

def selector_before_capture(t, c):
    """
    type = selector
    """
    c['selector_capture'] = []
    return t

def selector_after_capture(t, c):
    """
    type = selector
    """
    t['_main_tag'] = next(map(lambda a: a['type'] in ('quoted', 'osmtag') and a['value'] or None, c['selector_capture']))
    del(c['selector_capture'])
    return t


def rule_before_flags(t, c):
    """
    type = rule
    """
    c['flags'] = []
    return t

def functionExpression_rule_flags(t, c):
    """
    type = functionExpression
    waylength function need geo target
    """
    if t['name'] in ('waylength', 'areasize'):
        c['flags'].append('geo')
    elif t['name'] in ('JOSM_search', 'JOSM_pref'):
        c['flags'].append('josm')
    elif t['name'] in ('parent_tag', 'parent_tags', 'parent_osm_id'):
        c['flags'].append('relational')
    return t

def rule_after_flags(t, c):
    """
    type = rule
    """
    t['_flag'] = c['flags']
    del(c['flags'])
    return t

def rule_before_set(t, c):
    """
    type = rule
    """
    c['declare_set'] = set()
    c['use_set'] = set()
    return t

def declaration_declare_set(t, c):
    """
    type = declaration
    Track "set" declaration
    """
    c['declare_set'].add(t['set'])
    return t

def class_selector_use_set(t, c):
    """
    type = class_selector
    Track "set" usage
    """
    c['use_set'].add(t['class'])
    return t

def rule_after_set(t, c):
    """
    type = rule
    """
    t['_declare_set'] = c['declare_set']
    del(c['declare_set'])
    t['_require_set'] = c['use_set']
    del(c['use_set'])
    return t

rewrite_rules_clean = [
    ('valueExpression', valueExpression_remove_null_op),
    ('primaryExpression', primaryExpression_remove_null_op),
    ('quoted', quoted_unescape),
    ('regexExpression', regexExpression_unescape),
    ('simple_selector', simple_selector_pseudo_class),
    ('functionExpression', functionExpression_eval),
]

rewrite_rules_change_before = [
    # Rewrite
    ('primaryExpression', primary_expression_derefered),
    ('predicate_simple', predicate_simple_dereference),
    ('booleanExpression', booleanExpression_dereference_first_operand),
    ('booleanExpression', booleanExpression_capture_first_operand),
    ('booleanExpression', booleanExpression_negated_operator),
    ('booleanExpression', booleanExpression_operator_to_function),
    ('declaration_value_function', declaration_value_function_param_regex),
    # Safty
    ('rule', rule_declarations_order),
    # Rule flag
    ('selector', selector_before_capture),
    ('rule', rule_before_flags),
    ('functionExpression', functionExpression_rule_flags),
    # Set
    ('rule', rule_before_set),
    ('declaration', declaration_declare_set),
    ('class_selector', class_selector_use_set),
]
rewrite_rules_change_after = [
    # Rule flag
    ('selector', selector_after_capture),
    ('rule', rule_after_flags),
    # Set
    ('rule', rule_after_set),
]


def rewrite_tree_apply_rules(rules, t, c):
    for rule in rules:
        if t['type'] == rule[0]:
            t = rule[1](t, c)
    return t

def rewrite_tree_rules(before_rules, after_rules, t, c):
    if isinstance(t, str):
        return t
    elif isinstance(t, dict):
        if before_rules:
            t = rewrite_tree_apply_rules(before_rules, t, c)
        for k, v in t.items():
            t[k] = rewrite_tree_rules(before_rules, after_rules, v, c)
        if after_rules:
            t = rewrite_tree_apply_rules(after_rules, t, c)
    elif isinstance(t, list):
        t = list(map(lambda tt: rewrite_tree_rules(before_rules, after_rules, tt, c), t))
    return t

def rewrite_tree(t):
    t = rewrite_tree_rules(rewrite_rules_clean, None, t, {})
    t = rewrite_tree_rules(rewrite_rules_change_before, rewrite_rules_change_after, t, {})
    return t


def segregate_selectors_by_complexity(t):
    rules_complex = []
    rules_simple = []
    for rule in t['rules']:
        selector_complex = []
        selector_simple = []
        for selector in rule['selectors']:
            if selector['operator']:
                selector_complex.append(selector)
            elif next(filter(lambda a: not a in('closed', 'closed2', 'tagged'), selector['simple_selectors'][0]['pseudo_class']), False):
                selector_complex.append(selector)
            else:
                selector_simple.append(selector)
        if selector_complex != []:
            rules_complex.append(rule.copy())
            rules_complex[-1]['selectors'] = selector_complex
        if selector_simple != []:
            rules_simple.append(rule.copy())
            rules_simple[-1]['selectors'] = selector_simple

    return {'rules_complex': rules_complex, 'rules_simple': rules_simple}


def segregate_selectors_type(rules):
    out_rules = {'node': [], 'way': [], 'relation': []}
    for rule in rules:
        out_selector = {'node': [], 'way': [], 'relation': []}
        for selector in rule['selectors']:
            type_selector = selector['simple_selectors'][0]['type_selector']
            for t in 'node', 'way', 'relation':
                if type_selector == t or type_selector == '*':
                    out_selector[t].append(selector)
        for t in 'node', 'way', 'relation':
            if out_selector[t]:
                out_rules[t].append(rule.copy())
                out_rules[t][-1]['selectors'] = out_selector[t]
                out_rules[t][-1]['declarations'] = list(filter(lambda d: not d['property'] or not d['property'].startswith('assert') or (d['value']['type'] == 'single_value' and d['value']['value']['value'].startswith(t)), out_rules[t][-1]['declarations']))

    return dict(filter(lambda kv: len(kv[1]) > 0, out_rules.items()))


def stablehash(s):
    """
    Compute a stable positive integer hash on 32bits
    @param s: a string
    """
    return int(abs(int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)) % 2147483647)


class_map = {}
class_index = 0
class_id = group = group_class = text = text_class = fix = None
subclass_id = 0
class_ = {}
tests = []
regex_store = {}
set_store = set()
predicate_capture_index = 0
subclass_backlist = []

def to_p(t):
    global class_map, class_index, class_id, subclass_id, group, group_class, text, text_class, fix
    global tests, class_, regex_store, set_store
    global predicate_capture_index
    global subclass_backlist

    if isinstance(t, str):
        return t
    elif t['type'] == 'stylesheet':
        return "\n".join(map(to_p, t['rules']))
    elif t['type'] == 'rule':
        class_id = group = group_class = text = text_class = None # For safty
        selectors_text = "# " + "\n# ".join(map(lambda s: s['text'], t['selectors']))
        subclass_id = stablehash(selectors_text)
        if subclass_id in subclass_backlist:
            return selectors_text + "\n# Rule Blacklisted\n"
        elif t.get('_flag'):
            return selectors_text + "\n# Part of rule not implemented\n"
        elif not t['_require_set'].issubset(set_store):
            return selectors_text + "\n# Use undeclared class " + ", ".join(t['_require_set']) + "\n"
        else:
            main_tags = set(map(lambda s: s.get('_main_tag'), t['selectors']))
            fix = {'fixAdd': [], 'fixChangeKey': [], 'fixRemove': []}
            declarations_text = list(filter(lambda a: a, map(to_p, t['declarations'])))
            fix = dict(map(lambda kv: [{'fixAdd': '+', 'fixChangeKey': '~', 'fixRemove': '-'}[kv[0]], kv[1]], filter(lambda kv: len(kv[1]) > 0, fix.items())))
            fix = len(fix) > 0 and map(lambda om: "'" + om[0] + "': " + ("dict" if om[0] != '-' else "") + "([\n            " + ",\n            ".join(om[1]) + "])", sorted(fix.items()))
            return (
                selectors_text + "\n" +
                "if " +
                (("(" + " or ".join(map(lambda s: "u'" + s.replace("'", "\\'") + "' in keys", sorted(main_tags))) + ") and \\\n    ") if not None in main_tags else "") + # Quick fail
                "(" + " or \\\n    ".join(map(to_p, t['selectors'])) + "):\n" +
                "    # " + "\n    # ".join(filter(lambda a: a, map(lambda d: d['text'], t['declarations']))) + "\n" +
                (("    " + "\n    ".join(declarations_text) + "\n") if declarations_text else "") +
                (("    err.append({" +
                    "'class': " + str(class_id) + ", " +
                    "'subclass': " + str(subclass_id or 0) + ", " +
                    "'text': " + (text if text.startswith('mapcss.tr') else "{'en': " + text + "}") +
                    (", 'fix': {\n        " + ",\n        ".join(fix) + "\n    }" if fix else "") + "})\n")
                if text else "")
            )
    elif t['type'] == 'selector':
        if t['operator']:
            raise NotImplementedError(t)
        else:
            return " and ".join(map(to_p, t['simple_selectors']))
    elif t['type'] == 'link_selector':
        if t['role']:
            raise NotImplementedError(t)
        else: # t['index']
            raise NotImplementedError(t)
    elif t['type'] == 'simple_selector':
        # to_p(t['type_selector']) + Ignore
        sp = list(map(to_p, t['class_selectors']))
        predicate_capture_index = 0
        for predicate in t['predicates']:
            sp.append(to_p(predicate))
            predicate_capture_index += 1
        sp += list(map(to_p, t['pseudo_class']))
        return "(" + " and ".join(sp) + ")"
    elif t['type'] == 'class_selector':
        return ("not " if t['not'] else "") + "set_" + t['class']
    elif t['type'] == 'predicate_simple':
        return ("not " if t['not'] else "") + to_p(t['predicate']) + (" in ('yes', 'true', '1')" if t['question_mark'] else "")
    elif t['type'] == 'pseudo_class':
        if t['pseudo_class'] in ('closed', 'closed2', 'tagged'):
            raise NotImplementedError(t)
        else:
            raise NotImplementedError(t)
    elif t['type'] == 'declaration':
        if t['set']:
            s = t['set'] if t['set'][0] != '.' else t['set'][1:]
            set_store.add(s)
            return "set_" + s + " = True"
        else:
            if t['property'] == 'group':
                group = to_p(t['value'])
                group_class = t['value']['params'][0] if t['value']['type'] == 'declaration_value_function' and t['value']['name'] == 'tr' else t['value']
                group_class = group_class['value']['value'] if group_class['type'] == 'single_value' and group_class['value']['type'] == 'quoted' else to_p(group_class)
            elif t['property'] in ('throwError', 'throwWarning', 'throwOther'):
                text = to_p(t['value'])
                text_class = t['value']['params'][0] if t['value']['type'] == 'declaration_value_function' and t['value']['name'] == 'tr' else t['value']
                text_class = text_class['value']['value'] if text_class['type'] == 'single_value' and text_class['value']['type'] == 'quoted' else to_p(text_class)
                if (group_class or text_class) in class_map:
                    class_id = class_map[group_class or text_class]
                else:
                    class_index += 1
                    class_id = class_map[group_class or text_class] = class_index
                class_[class_id] = {'class': class_id, 'level': {'E': 1, 'W': 2, 'O': 3}[t['property'][5]], 'desc':
                    (group if group.startswith('mapcss.tr') else "{'en': " + group + "}") if group else
                    (text if text.startswith('mapcss.tr') else "{'en': " + text + "}")
                }
            elif t['property'] == 'suggestAlternative':
                pass # Do nothing
            elif t['property'] == 'fixAdd':
                if t['value']['type'] == 'single_value' and t['value']['value']['type'] == 'quoted':
                    fix[t['property']].append("[" + ','.join(map(lambda a: "u'" + a.strip().replace("'", "\\'") + "'", t['value']['value']['value'].split('=', 1))) + "]")
                else:
                    fix[t['property']].append("(" + to_p(t['value']) + ").split('=', 1)")
            elif t['property'] == 'fixChangeKey':
                if t['value']['type'] == 'single_value' and t['value']['value']['type'] == 'quoted':
                    l = t['value']['value']['value'].split('=>', 1)
                    fix['fixRemove'].append("u'" + l[0].strip().replace("'", "\\'") + "'")
                    fix['fixAdd'].append("[u'" + l[1].strip().replace("'", "\\'") + "', mapcss.tag(tags, u'" + l[0].strip().replace("'", "\\'") + "')]")
                else:
                    l = "(" + to_p(t['value']) + ").split('=>', 1)"
                    fix['fixRemove'].append(l + "[0].strip()")
                    fix['fixAdd'].append("[" + l + "[1].strip(), mapcss.tag(tags, " + l + "[0].strip())]")
            elif t['property'] == 'fixRemove':
                fix[t['property']].append(to_p(t['value']))
            elif t['property'] == 'fixDeleteObject':
                # raise NotImplementedError(t['property'])
                fix['fixRemove'] == "*keys" # TODO delete completly the objet in place of remove all tags
            elif t['property'].startswith('assert'):
                tests.append({'type': t['property'], 'what': to_p(t['value']), 'class': class_id, 'subclass': subclass_id or 0})
            else:
                raise NotImplementedError(t['property'])
    elif t['type'] == 'single_value':
        return to_p(t['value'])
    elif t['type'] == 'declaration_value_function':
        if t['name'] == 'tr' and (len(t['params']) == 1 or t['params'][1] != 'capture_tags'):
            t['params'] = t['params'][0:1] + ['capture_tags'] + t['params'][1:]
        return (
            ("mapcss.regexp_test_") if t['name'] == 'regexp_test' else
            ("mapcss." + t['name'])
        ) + "(" + (
            ("tags, " if t['name'] == 'tag' else "")
        ) + ", ".join(map(to_p, t['params'])) + ")"
    elif t['type'] == 'booleanExpression':
        if not t['operator']:
            return to_p(t['operands'][0])
        elif t['operator'] == '(':
            return "(" + to_p(t['operands'][0]) + ")"
        elif t['operator'] == '!':
            return "not " + to_p(t['operands'][0])
        elif t['operator'] in ('!~', '=~', '^=', '$=', '*=', '~='):
            raise NotImplementedError(t) # Done with rewrite_rules to function
        else:
            return (
                to_p(t['operands'][0]) + " " +
                {'||': 'or', '&&': 'and', '=': '=='}.get(t['operator'], t['operator']) + " " +
                to_p(t['operands'][1])
            )
    elif t['type'] == 'valueExpression':
        if t['operator'] == '(':
            return "(" + to_p(t['operands'][0]) + ")"
        if not t['operator']:
            return to_p(t['operands'][0])
        else:
            return to_p(t['operands'][0]) + t['operator'] + to_p(t['operands'][1])
    elif t['type'] == 'zoom_selector':
        return "" # Ignore
    elif t['type'] == 'quoted':
        return "u'" + t['value'].replace("'", "\\'") + "'"
    elif t['type'] == 'osmtag':
        return "u'" + t['value'] + "'"
    elif t['type'] == 'regexExpression':
        if t['value'] in regex_store:
            regex_var = regex_store[t['value']]
        else:
            regex_var = regex_store[t['value']] = "re_%08x" % stablehash(t['value'])
        return "self." + regex_var
    elif t['type'] == 'functionExpression':
        if t['name'] == 'osm_id':
            return "dada['id']"
        elif t['name'] == 'number_of_tags':
            return "len(tags)"
        elif t['name'] == 'at':
            return "(data['lat'] == " + to_p(t['params'][0]) + " and data['lon'] == " + to_p(t['params'][1]) + ")"
        else:
            if t['name'] == 'tr' and (len(t['params']) == 1 or t['params'][1] != 'capture_tags'):
                t['params'] = t['params'][0:1] + ['capture_tags'] + t['params'][1:]
            return (
                ("keys.__contains__") if t['name'] == 'has_tag_key' else
                ("mapcss.regexp_test_") if t['name'] == 'regexp_test' else
                ("mapcss." + t['name'])
            ) + "(" + (
                ("tags, " if t['name'] == 'tag' else "") +
                ("self.father.config.options, " if t['name'] in ('inside', 'outside') else "") +
                (("capture_tags, " + str(predicate_capture_index) + ", tags, ") if t['name'] == '_tag_capture' else "")
            ) + ", ".join(map(to_p, t['params'])) + ")"
    elif t['type'] == 'primaryExpression':
        if t['derefered']:
            raise NotImplementedError(t) # Done with rewrite_rules
        return to_p(t['value'])
    else:
        return "<UNKNOW TYPE {0}>".format(t['type'])


def build_items(item, class_):
    out = []
    for _, c in sorted(class_.items(), key = lambda a: a[0]):
        out.append("self.errors[" + str(c['class']) + "] = {'item': " + str(item) + ", 'level': " + str(c['level']) + ", 'tag': [], 'desc': " + c['desc'] + "}")
    return "\n".join(out)

def build_tests(tests):
    kv_split = re.compile('([^= ]*=)')
    out = []
    for test in tests:
        okvs = list(map(lambda s: s.strip(' ='), kv_split.split(test['what'][2:-1])))
        o, kvs = okvs[0], list(map(lambda a: a[0] in '"\'' and a[0] == a[-1] and a[1:-1] or a, map(lambda a: a.replace('\\\"', '"').replace("\\\'", "'"), okvs[1:])))
        kvs = zip(kvs[0::2], kvs[1::2]) # kvs.slice(2)
        tags = dict(kvs)
        out.append(
            "self." + ("check_err" if test['type'] == 'assertMatch' else "check_not_err") + "(" +
                "n." + o + "(data, {" + ', '.join(map(lambda kv: "u'" + kv[0].replace("'", "\\'") + "': u'" + kv[1].replace("'", "\\'") + "'", sorted(tags.items()))) + "}), " +
                "expected={'class': " + str(test['class']) + ", 'subclass': " + str(test['subclass']) + "})"
        )
    return "\n".join(out)


from item_map import item_map

def main(_, mapcss):
    path = os.path.dirname(mapcss)
    class_name = original_class_name = '.'.join(os.path.basename(mapcss).replace('.validator.', '.').split('.')[:-1])
    global class_map, subclass_backlist
    if class_name in item_map:
        i = item_map[class_name]
        item = i['item']
        class_map = i.get('class', {})
        subclass_backlist = i.get('subclass_backlist', {})
        only_for = i.get('only_for', [])
        prefix = i.get('prefix', '')
    else:
        item = 0
        class_map = {}
        subclass_backlist = []
        only_for = []
        prefix = ''
    class_name = class_name.replace('.', '_').replace('-', '_')
    global class_index
    class_index = item * 1000

    input = FileStream(mapcss, encoding='utf-8')
    lexer = MapCSSLexer(input)
    stream = CommonTokenStream(lexer)
    parser = MapCSSParser(stream)
    tree = parser.stylesheet()

    listener = MapCSSListenerL()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    selectors_by_complexity = segregate_selectors_by_complexity(listener.stylesheet)
    tree = rewrite_tree(selectors_by_complexity['rules_simple'])
    selectors_type = segregate_selectors_type(tree)

    global class_, tests, regex_store, set_store
    rules = dict(map(lambda t: [t, to_p({'type': 'stylesheet', 'rules': selectors_type[t]})], sorted(selectors_type.keys(), key = lambda a: {'node': 0, 'way': 1, 'relation':2}[a])))
    items = build_items(item, class_)
    asserts = build_tests(tests)

    mapcss = ("""#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_""" + prefix + class_name + """(Plugin):
""" + ("\n    only_for = ['" + "', '".join(only_for) + "']\n" if only_for != [] else "") + """
    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        """ + items.replace("\n", "\n        ") + """
        """ + "".join(map(lambda r: """
        self.""" + r[1] + " = re.compile(ur'" + r[0].replace('(?U)', '').replace("'", "\\'") + "')", sorted(regex_store.items(), key = lambda s: s[1]))) + """

""" + "".join(map(lambda t: """
    def """ + t + """(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []
        """ + ((" = ".join(list(map(lambda s: "set_" + s, sorted(set_store)))) + " = False") if len(set_store) > 0 else "") + """

        """ + rules[t].replace("\n", "\n        ") + """
        return err
""", sorted(rules.keys(), key = lambda a: {'node': 0, 'way': 1, 'relation':2}[a]))) + """

from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_""" + prefix + class_name + """(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        """ + asserts.replace("\n", "\n        ") + """
""").replace("        \n", "\n")
    f = open((path or '.') + '/MapCSS_' + prefix + class_name + '.py', 'w')
    f.write(mapcss)
    f.close()

    if original_class_name in item_map:
        item_map[original_class_name]['class'] = class_map
        f = open("item_map.py", "w")
        f.write("item_map = \\\n")
        pprint(item_map, f)
        f.close()

if __name__ == '__main__':
    main(*sys.argv)
