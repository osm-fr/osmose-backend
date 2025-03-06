#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import os
import re
import ast
from modules.Stablehash import stablehash
from pprint import pprint
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from .generated.MapCSSLexer import MapCSSLexer
from .generated.MapCSSParser import MapCSSParser
from .MapCSSListenerL import MapCSSListenerL
from typing import Dict, List, Set, Optional, Union
from copy import deepcopy
from . import mapcss_lib
from inspect import signature, Parameter


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

def valueExpression_equal(t, c):
    """
    type = valueExpression
    Use only '=' as equal opperator
    """
    if t['operator'] and t['operands'] == '==':
        t['operands'] = '='
    return t

def quoted_unescape(t, c):
    """
    type = quoted
    Remove surrounding quotes and unescape content
    """
    if not 'unescape' in t:
        t['unescape'] = True
        t['value'] = ast.literal_eval(t['value'])
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
    Remove always true pseudo class
    """
    t['pseudo_class'] = list(filter(lambda p: not (p['not_class'] and p['pseudo_class'] in ('completely_downloaded', 'in-downloaded-area')), t['pseudo_class']))
    return t

def convert_area_selectors(t, c):
    """
    type = rule
    Convert area* rules to way[area!=no]* + relation[type=multipolygon]*
    """
    areaselectors = list(filter(lambda selector: selector['simple_selectors'][0]['type_selector'] == 'area', t['selectors']))
    for s in areaselectors:
        relSelector = deepcopy(s)
        relSelector['simple_selectors'][0]['type_selector'] = 'relation'
        extra_predicate = deepcopy(mock_rules['type_eq_multipolygon'])
        extra_predicate.update({'selector_index': selector_index_map['arearule']})
        relSelector['simple_selectors'][0]['predicates'].append(extra_predicate)
        t['selectors'].append(relSelector)

        s['simple_selectors'][0]['type_selector'] = 'way'
        extra_predicate = deepcopy(mock_rules['area_neq_no'])
        extra_predicate.update({'selector_index': selector_index_map['arearule']})
        s['simple_selectors'][0]['predicates'].append(extra_predicate)
    return t

def convert_closed_pseudo_relation_node(t, c):
    """
    type = rule
    Convert relation:closed/closed2 to [type=multipolygon]
    Multipolygon relations are always closed, nodes and other relations are always open
    (Technically partially downloaded multipolygons aren't closed2)
    """

    for selector in t['selectors']:
        type_selector = selector['simple_selectors'][0]['type_selector']
        if type_selector not in ('node', 'relation'):
            continue

        if type_selector == 'node':
            selector.update({'pseudo_class': list(filter(lambda p: not (p['not_class'] and p['pseudo_class'] in ('closed', 'closed2')), selector['pseudo_class']))})
            selector['simple_selectors'][0]['pseudo_class'] = list(filter(lambda p: not (p['not_class'] and p['pseudo_class'] in ('closed', 'closed2')), selector['pseudo_class']))
        if type_selector == 'relation':
            isPseudoClosed = any(map(lambda p: p['pseudo_class'] in ('closed', 'closed2') and not p['not_class'], selector['pseudo_class']))
            isPseudoNotClosed = any(map(lambda p: p['pseudo_class'] in ('closed', 'closed2') and p['not_class'], selector['pseudo_class']))
            selector.update({'pseudo_class': list(filter(lambda p: not p['pseudo_class'] in ('closed', 'closed2'), selector['pseudo_class']))})
            selector['simple_selectors'][0]['pseudo_class'] = list(filter(lambda p: not p['pseudo_class'] in ('closed', 'closed2'), selector['pseudo_class']))
            if isPseudoClosed:
                extra_predicate = deepcopy(mock_rules['type_eq_multipolygon'])
                extra_predicate.update({'selector_index': selector_index_map['closedrelation']})
                selector['simple_selectors'][0]['predicates'].append(extra_predicate)
            if isPseudoNotClosed:
                extra_predicate = deepcopy(mock_rules['type_neq_multipolygon'])
                extra_predicate.update({'selector_index': selector_index_map['closedrelation']})
                selector['simple_selectors'][0]['predicates'].append(extra_predicate)

    return t

def functionExpression_eval(t, c):
    """
    type = functionExpression
    Remove call to eval
    """
    if t['name'] == 'eval':
        t = t['params'][0]
    return t

def rule_exclude_throw_other(t, c):
    """
    type = rule
    Remove throwOther
    """
    if not next(filter(lambda declaration: declaration['property'] and declaration['property'] == '-osmoseItemClassLevel', t['declarations']), False):
        t['declarations'] = list(filter(lambda declaration: not declaration['property'] or declaration['property'] != 'throwOther', t['declarations']))
    return t

def rule_exclude_unsupported_meta(t, c):
    """
    type = rule
    Remove declaration no supported from meta rule
    """
    if t['selectors'][0]['simple_selectors'][0]['type_selector'] == 'meta':
        t['_meta'] = True
        t['declarations'] = list(filter(lambda declaration: not declaration['property'] or declaration['property'] in ('-osmoseTags',), t['declarations']))
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
    t['predicate'] = {'type': 'functionExpression', 'name': '_tag_capture', 'params': ['capture_tags', str(t['selector_index']), 'tags', t['predicate']]}
    return t

def booleanExpression_dereference_first_operand(t, c):
    """
    type = booleanExpression
    Replace first operand by the value of the tag
    """
    if len(t['operands']) >= 1 and t['operands'][0]['type'] in ('osmtag', 'quoted'):
        t['operands'][0] = {'type': 'functionExpression', 'name': 'maintag', 'params': [t['operands'][0]]}
    return t

def booleanExpression_capture_first_operand(t, c):
    """
    type = booleanExpression
    Capture first operand tag
    """
    if len(t['operands']) >= 1 and t['operands'][0]['type'] == 'functionExpression' and t['operands'][0]['name'] == 'maintag':
        if not t['operator'] in ('!', '!=', '!~'):
            c['selector_capture'].append(t['operands'][0]['params'][0])
        t['operands'][0] = {'type': 'functionExpression', 'name': '_tag_capture', 'params': ['capture_tags', str(t['selector_index']), 'tags', t['operands'][0]['params'][0]]}
        if t['operator'] in ('!', '!=', '!~') and t['operands'][1]['type'] in ('quoted', 'osmtag', 'regexExpression'):
            t['operands'][1] = {'type': 'functionExpression', 'name': '_value_const_capture', 'params': ['capture_tags', str(t['selector_index']), t['operands'][1], {'type': 'quoted', 'value': str(t['operands'][1]['value'])}]}
        else:
            t['operands'][1] = {'type': 'functionExpression', 'name': '_value_capture', 'params': ['capture_tags', str(t['selector_index']), t['operands'][1]]}
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
    operands_0 = t['operands'][0]
    if operands_0['type'] == 'regexExpression':
        operands_0 = {'type': 'functionExpression', 'name': '_match_regex', 'params': ['tags', operands_0]}
    if t['operator'] == '=~':
        t = {'type': 'functionExpression', 'name': booleanExpression_operator_to_function_map[t['operator']], 'params': [
            t['operands'][1],
            operands_0
        ]}
    elif t['operator'] in booleanExpression_operator_to_function_map.keys():
        # Direct prams order
        t = {'type': 'functionExpression', 'name': booleanExpression_operator_to_function_map[t['operator']], 'params': [
            operands_0,
            t['operands'][1]
        ]}
    return t

def functionExpression_param_regex(t, c):
    """
    type = functionExpression
    Ensure params to regex functions are regex
    """
    if t['name'] in ('regexp_test', 'regexp_match', 'tag_regex'):
        if t['params'][0]['type'] == 'quoted':
            t['params'][0] = {'type': 'regexExpression', 'value': t['params'][0]['value']}
    return t

def functionExpression_regexp_flags(t, c):
    """
    type = functionExpression
    Move regex flag from match function to regex object
    """
    if t['name'] in ('regexp_test', 'regexp_match', 'tag_regex') and len(t['params']) == 3:
        flags = t['params'].pop()
        t['params'][0]['params'][2]['flags'] = flags
    return t

def pseudo_class_righthandtraffic(t, c):
    """
    type = pseudo_class
    Replace pseudo class :righthandtraffic by call to setting()
    """
    if t['pseudo_class'] == 'righthandtraffic':
        setting_selector = deepcopy(mock_rules['setting_drivingside_eq_left' if t['not_class'] else 'setting_drivingside_neq_left'])
        setting_selector = rewrite_tree_rules(rewrite_rules_clean, None, setting_selector, {})
        setting_selector['selector_index'] = t.get('selector_index')
        return setting_selector
    return t

rule_declarations_order_map = {
    # subclass
    'group': 1,
    # Osmose
    '-osmoseItemClassLevel': 2,
    '-osmoseTags': 2,
    '-osmoseDetail': 2,
    '-osmoseTrap': 2,
    '-osmoseFix': 2,
    '-osmoseExample': 2,
    '-osmoseResource': 2,
    # text
    'throwError': 3,
    'throwWarning': 3,
    'throwOther': 3,
    'suggestAlternative': 3,
    # fix
    'fixAdd': 4,
    'fixChangeKey': 4,
    'fixRemove': 4,
    'fixDeleteObject': 4,
    # test
    'assertMatch': 5,
    '-osmoseAssertMatchWithContext': 5,
    'assertNoMatch': 5,
    '-osmoseAssertNoMatchWithContext': 5,
}

def rule_declarations_order(t, c):
    """
    type = rule
    Order the declarations in order attended by the code generator
    """
    t['declarations'] = sorted(t['declarations'], key = lambda d: (d.get('property') and [rule_declarations_order_map.get(d['property']) or print("W: Unknown property: " + d['property']) and -1, str(d['value'])]) or [-1, -1])
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
    t['_main_tags'] = list(map(lambda a: a['type'] in ('quoted', 'osmtag') and a['value'] or None, c['selector_capture']))
    del c['selector_capture']
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

specialCountryMap = {
    # https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#exceptional-reservations
    # None here simply means 'not yet implemented by us'
    'AC': None,
    'CP': None,
    'CQ': None,
    'DG': None,
    'EA': None,
    'EU': None,
    'EZ': None,
    'FX': ['FR-69M', 'FR-69D', 'FR-2A', 'FR-2B'] + list(map(lambda n: 'FR-{:02}'.format(n), range(1,96))),
    'IC': None,
    'SU': None,
    'TA': None,
    'UK': None,
    'UN': None,
}
def functionExpression_insideoutside(t, c):
    """
    type = functionExpression
    convert unconventional country codes to Osmose equivalent
    """
    if t['name'] in ('inside', 'outside'):
        countries = t["params"][0]["value"].split(',')
        countries = list(map(lambda x: x if x not in specialCountryMap or (specialCountryMap[x] is None and not print("Warning: special country code not implemented yet: " + x)) else ','.join(specialCountryMap[x]), countries))
        t["params"][0]["value"] = ','.join(countries)
    return t

def rule_after_flags(t, c):
    """
    type = rule
    """
    t['_flag'] = c['flags']
    del c['flags']
    return t

def rule_before_set(t, c):
    """
    type = rule
    """
    c['declare_set'] = set()
    return t

def selector_before_use_set(t, c):
    """
    type = rule
    """
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
    del c['declare_set']
    return t

def selector_after_use_set(t, c):
    """
    type = selector
    """
    t['_require_set'] = c['use_set']
    del c['use_set']
    return t

def quoted_uncapture(t, c):
    """
    type = quoted
    Add arround function to capture tag key and value
    """
    if '.tag}' in t['value'] or '.key}' in t['value'] or '.value}' in t['value']:
        t = {'type': 'functionExpression', 'name': '_tag_uncapture', 'params': ["capture_tags", t]}
    return t

def functionExpression_runtime(t, c):
    """
    type = functionExpression
    Add runtime python parameter and function name
    """
    if t['name'] == 'osm_id':
        return "data['id']"
    elif t['name'] == 'number_of_tags':
        return "len(tags)"
    else:
        t['params'] = (
            ["tags"] if t['name'] in ('tag', 'tag_regex') else
            ["data['lat']", "data['lon']"] if t['name'] == 'at' else
            ["self.father.config.options"] if t['name'] in ('inside', 'outside', 'language', 'no_language', 'setting') else
            []
        ) + t['params']

        t['name'] = (
            "keys.__contains__" if t['name'] == 'has_tag_key' else
            "mapcss.list_" if t['name'] == 'list' else
            "mapcss.any_" if t['name'] == 'any' else
            "mapcss.round_" if t['name'] == 'round' else
            "mapcss." + t['name']
        )

        if not c.get('flags'):
            checkValidFunction(t['name'], len(t['params']))
    return t

def checkValidFunction(fn_name, num_params):
    """
    Tests if mapcss.* functions actually exist, throws a compile error otherwise
    """
    if fn_name[0:7] != "mapcss.":
        return
    if not fn_name[7:] in dir(mapcss_lib):
        raise NotImplementedError("Undefined function '{0}'. Blacklist or implement to avoid errors".format(fn_name))
    else:
        sig = signature(getattr(mapcss_lib, fn_name[7:]))
        argcount = len(sig.parameters) # includes optional arguments
        has_vararg = any(map(lambda p: p.kind == Parameter.VAR_POSITIONAL, sig.parameters.values()))
        num_optional_arg = len(set(filter(lambda p: p.default != Parameter.empty, sig.parameters.values())))
        if has_vararg:
            argcount = argcount - 1 # *args can be zero-length
        if num_params < argcount - num_optional_arg or (not has_vararg and num_params > argcount):
            raise NotImplementedError("Undefined function '{0}' with {1} arguments. Blacklist or implement to avoid errors".format(fn_name, num_params))


rewrite_rules_clean = [
    ('valueExpression', valueExpression_remove_null_op),
    ('primaryExpression', primaryExpression_remove_null_op),
    ('valueExpression', valueExpression_equal),
    ('quoted', quoted_unescape),
    ('regexExpression', regexExpression_unescape),
    ('simple_selector', simple_selector_pseudo_class),
    ('rule', convert_area_selectors),
    ('rule', convert_closed_pseudo_relation_node),
    ('functionExpression', functionExpression_eval),
    ('rule', rule_exclude_throw_other),
    ('rule', rule_exclude_unsupported_meta),
]

rewrite_rules_change_before = [
    # Rewrite
    ('primaryExpression', primary_expression_derefered),
    ('predicate_simple', predicate_simple_dereference),
    ('booleanExpression', booleanExpression_dereference_first_operand),
    ('booleanExpression', booleanExpression_capture_first_operand),
    ('booleanExpression', booleanExpression_negated_operator),
    ('booleanExpression', booleanExpression_operator_to_function),
    ('functionExpression', functionExpression_param_regex),
    ('functionExpression', functionExpression_regexp_flags),
    ('functionExpression', functionExpression_insideoutside),
    ('pseudo_class', pseudo_class_righthandtraffic),
    # Safty
    ('rule', rule_declarations_order),
    # Rule flag
    ('selector', selector_before_capture),
    ('rule', rule_before_flags),
    ('functionExpression', functionExpression_rule_flags),
    # Set
    ('rule', rule_before_set),
    ('declaration', declaration_declare_set),
    ('selector', selector_before_use_set),
    ('class_selector', class_selector_use_set),
]
rewrite_rules_change_after = [
    # Rule flag
    ('selector', selector_after_capture),
    ('rule', rule_after_flags),
    # Set
    ('rule', rule_after_set),
    ('selector', selector_after_use_set),
    # Pythonize
    ('quoted', quoted_uncapture),
    ('functionExpression', functionExpression_runtime),
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
    rules_meta = []
    rules_complex = []
    rules_simple = []
    for rule in t['rules']:
        if rule.get('_meta'):
            rules_meta.append(rule.copy())
        else:
            selector_complex = []
            selector_simple = []
            for selector in rule['selectors']:
                if selector['operator']:
                    selector_complex.append(selector)
                elif any(map(lambda a: not a['pseudo_class'] in ('closed', 'closed2', 'righthandtraffic'), selector['simple_selectors'][0]['pseudo_class'])):
                    selector_complex.append(selector)
                else:
                    selector_simple.append(selector)
            if selector_complex != []:
                rules_complex.append(rule.copy())
                rules_complex[-1]['selectors'] = selector_complex
            if selector_simple != []:
                rules_simple.append(rule.copy())
                rules_simple[-1]['selectors'] = selector_simple

    return {'rules_meta': rules_meta, 'rules_complex': rules_complex, 'rules_simple': rules_simple}


def segregate_selectors_type(rules):
    out_rules = {'node': [], 'way': [], 'relation': []}
    for rule in rules:
        if rule.get('_meta'):
            for t in 'node', 'way', 'relation':
                out_rules[t].append(rule.copy())
        else:
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
                    out_rules[t][-1]['declarations'] = list(filter(lambda d:
                        not d['property'] or not (d['property'].startswith('assert') or d['property'].startswith('-osmoseAssert')) or
                        (d['value']['type'] == 'single_value' and d['value']['value']['value'].startswith(t)) or
                        (d['value']['type'] == 'functionExpression' and d['value']['params'][0]['value'].startswith(t)),
                        out_rules[t][-1]['declarations']))

    return dict(filter(lambda kv: next(filter(lambda rule: not rule.get('_meta'), kv[1]), False), out_rules.items()))


def filter_non_productive_rules(rules):
    return list(filter(lambda rule:
        rule.get('_meta') or
        next(filter(lambda declaration: (declaration['property'] and declaration['property'].startswith('throw')) or declaration['set'], rule['declarations']), None) or print("W: Skip non productive rule"),
        rules))


def filter_osmose_none_rules(rules):
    return list(filter(lambda rule:
        rule.get('_meta') or
        not next(filter(lambda declaration: declaration.get('property') == '-osmoseItemClassLevel' and declaration['value'].get('type') == 'single_value' and declaration['value']['value']['value'] == 'none', rule['declarations']), None),
        rules))


def filter_typeselector_rules(rules):
    return list(filter(lambda rule: rule.get('_meta') or len(rule['selectors']) > 0, map(lambda rule:
        rule.get('_meta') and rule or
        rule.update({'selectors': list(filter(lambda selector: selector['simple_selectors'][0]['type_selector'] in ('node', 'way', 'relation', '*') or print("W: Skip unknown type selector"), rule['selectors']))}) or rule,
        rules
    )))

def filter_support_rules(rules):
    # We don't parse the actual values of @supports
    # Assume all rules within @supports {} are unsafe unless -osmoseItemClassLevel is set
    return list(filter(lambda rule:
        rule.get('_meta') or
        not rule.get('in_supports_declaration') or
        next(filter(lambda declaration: declaration.get('property') == '-osmoseItemClassLevel', rule['declarations']), None),
        rules))


class_map: Dict[Optional[str], int] = {}
class_index = 0
meta_tags = None
item_default = None
item = class_id = level = tags = group = group_class = text = text_class = fix = None
class_info_text = {}
subclass_id = 0
class_: Dict[str, Union[str, int, Dict[str, List[str]]]] = {}
tests = []
regex_store: Dict[List[str], str] = {}
set_store: Set[str] = set()
subclass_blacklist = []
is_meta_rule = False

def to_p(t):
    global item_default
    global class_map, class_index, meta_tags, item, class_id, level, tags, subclass_id, group, group_class, text, text_class, fix, class_info_text
    global tests, class_, regex_store, set_store
    global subclass_blacklist
    global is_meta_rule

    if isinstance(t, str):
        return t
    elif t['type'] == 'stylesheet':
        return "\n".join(filter(lambda s: s != "", map(to_p, t['rules'])))
    elif t['type'] == 'rule':
        item = class_id = level = tags = group = group_class = text = text_class = None # For safety
        is_meta_rule = t.get('_meta')
        selectors_text = "# " + "\n# ".join(map(lambda s: s['text'], t['selectors']))
        subclass_id = stablehash(selectors_text)
        if subclass_id in subclass_blacklist:
            return selectors_text + "\n# Rule Blacklisted (id: {0})\n".format(subclass_id)
        elif t.get('_flag'):
            return selectors_text + "\n# Part of rule not implemented\n"
        elif not is_meta_rule:
            main_tags = tuple(set(map(lambda s: tuple(set(filter(lambda z: z is not None, s.get('_main_tags')))), t['selectors'])))
            main_tags_None = any(map(lambda s: len(s) == 0, main_tags))
            fix = {'fixAdd': [], 'fixChangeKey': [], 'fixRemove': []}
            declarations_text = list(filter(lambda a: a, map(to_p, t['declarations'])))
            fix = dict(map(lambda kv: [{'fixAdd': '+', 'fixChangeKey': '~', 'fixRemove': '-'}[kv[0]], kv[1]], filter(lambda kv: len(kv[1]) > 0, fix.items())))
            fix = len(fix) > 0 and map(lambda om: "'" + om[0] + "': " + ("dict" if om[0] != '-' else "") + "([\n            " + ",\n            ".join(om[1]) + "])", sorted(fix.items()))
            return (
                selectors_text + "\n" +
                (("if (" + ") or (".join(sorted(map(lambda s: " and ".join(map(lambda z: "'" + z.replace("'", "\\'") + "' in keys", sorted(s))), main_tags))) + ")") if not main_tags_None else "if True") + ":\n" + # Quick fail
                "    match = False\n" +
                "".join(map(to_p, t['selectors'])) +
                "    if match:\n" +
                "        # " + "\n        # ".join(filter(lambda a: a, map(lambda d: d['text'], t['declarations']))) + "\n" +
                (("        " + "\n        ".join(declarations_text) + "\n") if declarations_text else "") +
                (("        err.append({" +
                    "'class': " + str(class_id) + ", " +
                    "'subclass': " + str(subclass_id or 0) + ", " +
                    "'text': " + (text if text.startswith('mapcss.tr') else "{'en': " + text + "}") +
                    (", 'allow_fix_override': True" if fix else "") +
                    (", 'fix': {\n            " + ",\n            ".join(fix) + "\n        }" if fix else "") + "})\n")
                if text else "")
            )
        elif is_meta_rule:
            list(map(to_p, t['declarations']))
            return ""
    elif t['type'] == 'selector':
        if t['operator']:
            raise NotImplementedError(t)
        elif not t['_require_set'].issubset(set_store):
            return "    # Skip selector using undeclared class " + ", ".join(sorted(t['_require_set'])) + "\n"
        else:
            return (
                "    if not match:\n" +
                "        capture_tags = {}\n" +
                "        try: match = " + " and ".join(map(to_p, t['simple_selectors'])) + "\n" +
                "        except mapcss.RuleAbort: pass\n"
            )
    elif t['type'] == 'link_selector':
        if t['role']:
            raise NotImplementedError(t)
        else: # t['index']
            raise NotImplementedError(t)
    elif t['type'] == 'simple_selector':
        # to_p(t['type_selector']) + Ignore
        sp = list(map(to_p, t['class_selectors'])) + list(map(to_p, t['predicates'])) + list(map(to_p, t['pseudo_class']))
        return "((" + ") and (".join(sp) + "))"
    elif t['type'] == 'class_selector':
        return ("not " if t['not'] else "") + "set_" + t['class']
    elif t['type'] == 'predicate_simple':
        return (
            ("not " if t['not'] else "") + to_p(t['predicate']) +
            ((" not" if t['question_mark_negated'] else "") + " in ('yes', 'true', '1')" if t['question_mark'] or t['question_mark_negated'] else "")
        )
    elif t['type'] == 'pseudo_class':
        if t['pseudo_class'] in ('closed', 'closed2'):
            return "nds[0] != nds[-1]" if t['not_class'] else "nds[0] == nds[-1]"
        else:
            raise NotImplementedError(t)
    elif t['type'] == 'declaration':
        if t['set']:
            s = t['set'] if t['set'][0] != '.' else t['set'][1:]
            set_store.add(s)
            return "set_" + s + " = True"
        # Meta info properties
        elif t['property'] == '-osmoseTags':
            if is_meta_rule:
                meta_tags = to_p(t['value'])
            else:
                tags = to_p(t['value'])
        # Standard propoerties
        elif t['property'] == 'group':
            group = to_p(t['value'])
            group_class = t['value']['params'][0] if t['value']['type'] == 'functionExpression' and t['value']['name'] == 'mapcss.tr' else t['value']
            group_class = group_class['value']['value'] if group_class['type'] == 'single_value' and group_class['value']['type'] == 'quoted' else to_p(group_class['value'])
        elif t['property'] == '-osmoseItemClassLevel':
            item, class_id, level = t['value']['value']['value'].split('/')
            item, class_id, subclass_id, level = int(item), int(class_id.split(':')[0]), ':' in class_id and int(class_id.split(':')[1]), int(level)
        elif t['property'] in ('-osmoseDetail', '-osmoseTrap', '-osmoseFix', '-osmoseResource', '-osmoseExample'):
            whichMsg = t['property'][7:].lower()
            text = to_p(t['value'])
            if t['value']['type'] == 'functionExpression' and t['value']['name'] == 'mapcss.tr':
                class_info_text[whichMsg] = text
            elif whichMsg == 'resource':
                class_info_text[whichMsg] = text # hyperlink as string, no need for language
            else:
                class_info_text[whichMsg] = '{"en": ' + text + '}'
        elif t['property'] in ('throwError', 'throwWarning', 'throwOther'):
            text = to_p(t['value'])
            text_class = t['value']['params'][0] if t['value']['type'] == 'functionExpression' and t['value']['name'] == 'mapcss.tr' else t['value']
            text_class = text_class['value']['value'] if text_class['type'] == 'single_value' and text_class['value']['type'] == 'quoted' else to_p(text_class['value'])
            if not class_id:
                if (group_class or text_class) in class_map:
                    class_id = class_map[group_class or text_class]
                else:
                    class_index += 1
                    class_id = class_map[group_class or text_class] = class_index
            else:
                # Store assigned id's (via -osmoseItemClassLevel) in None. They are not mapped to strings as this would lead to undefined behavior if
                # there is an entry with for instance -osmoseExample, which would (depending on sequence) be overwritten by an entry without -osmose*
                # properties, yet with the same group_class or text_class. Using None makes sure these get a unique id (as the max value is used for
                # determining the class_index.
                class_map[None] = max(class_map.get(None, 0), class_id)

            classInfoNew = {
                'item': item or item_default,
                'class': class_id,
                'level': level or {'E': 2, 'W': 3, 'O': None}[t['property'][5]],
                'tags': " + ".join(filter(lambda a: a, [meta_tags, tags])) or "[]",
                'desc':
                    (group if group.startswith('mapcss.tr') else "{'en': " + group + "}") if group else
                    (text if text.startswith('mapcss.tr') else "{'en': " + text + "}"),
                'info': class_info_text.copy()
            }
            normFn = lambda x: str(x).replace(" ", "").replace("'", '"').split('",')[0] if str(x).startswith('mapcss.tr') else str(x)
            if class_id in class_ and any([normFn(class_[class_id][x]) != normFn(classInfoNew[x]) for x in ('item', 'tags', 'desc', 'info')]):
                # Accept that e.g. level may differ, which can happen with the JOSM entries having the same message with throwError/throwWarning
                # Also remove everything after a ", because currently tr("xyz", "km") and tr("xyz", "kg") are in the same group, see also #1530
                # This will raise if e.g. the same class is used for two different messages.
                raise Exception("Overwriting class with different properties for class id {0}".format(str(class_id)))
            class_[class_id] = classInfoNew
            class_info_text = {}
        elif t['property'] == 'suggestAlternative':
            pass # Do nothing
        elif t['property'] == 'fixAdd':
            if t['value']['type'] == 'single_value' and t['value']['value']['type'] == 'quoted':
                fix[t['property']].append("[" + ','.join(map(lambda a: "'" + a.strip().replace("'", "\\'") + "'", t['value']['value']['value'].split('=', 1))) + "]")
            else:
                fix[t['property']].append("(" + to_p(t['value']) + ").split('=', 1)")
        elif t['property'] == 'fixChangeKey':
            if t['value']['type'] == 'single_value' and t['value']['value']['type'] == 'quoted':
                l = t['value']['value']['value'].split('=>', 1)
                fix['fixRemove'].append("'" + l[0].strip().replace("'", "\\'") + "'")
                fix['fixAdd'].append("['" + l[1].strip().replace("'", "\\'") + "', mapcss.tag(tags, '" + l[0].strip().replace("'", "\\'") + "')]")
            else:
                l = "(" + to_p(t['value']) + ").split('=>', 1)"
                fix['fixRemove'].append(l + "[0].strip()")
                fix['fixAdd'].append("[" + l + "[1].strip(), mapcss.tag(tags, " + l + "[0].strip())]")
        elif t['property'] == 'fixRemove':
            fix[t['property']].append(to_p(t['value']))
        elif t['property'] == 'fixDeleteObject':
            # raise NotImplementedError(t['property'])
            fix['fixRemove'] == "*keys" # TODO delete the object completely in place of removing all tags
        elif t['property'].startswith('assert') or t['property'].startswith('-osmoseAssert'):
            if t['value']['type'] == 'single_value':
                what, context = (to_p(t['value']), None)
            else: # It's a list (we hope so)
                what, context = (to_p(t['value']['params'][0]), to_p(t['value']['params'][1])[1:-1])
            tests.append({'type': t['property'], 'what': what, 'context': context, 'class': class_id, 'subclass': subclass_id or 0})
        else:
            raise NotImplementedError(t['property'])
    elif t['type'] == 'single_value':
        return to_p(t['value'])
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
        return "'" + t['value'].replace('\\', '\\\\').replace("'", "\\'") + "'"
    elif t['type'] == 'osmtag':
        return "'" + t['value'] + "'"
    elif t['type'] == 'regexExpression':
        if t['value'] in regex_store:
            regex_var = regex_store[t['value'], t.get('flags')]
        else:
            regex_var = regex_store[t['value'], t.get('flags')] = "re_%08x" % stablehash(t['value'] + t.get('flags', ''))
        return "self." + regex_var
    elif t['type'] == 'functionExpression':
        return t['name'] + "(" + ", ".join(map(to_p, t['params'])) + ")"
    elif t['type'] == 'primaryExpression':
        if t['derefered']:
            raise NotImplementedError(t) # Done with rewrite_rules
        return to_p(t['value'])
    else:
        return "<UNKNOWN TYPE {0}>".format(t['type'])


def build_items(class_):
    out = []
    for _, c in sorted(class_.items(), key = lambda a: a[0]):
        out.append("self.errors[" + str(c['class']) + "] = self.def_class(item = " + str(c['item']) +
        ", level = " + str(c['level']) + ", tags = " + c['tags'] + ", title = " + c['desc'] +
        "".join([', %s = %s' % (k,v) for k,v in c['info'].items()]) + ")")
    return "\n".join(out)

context_map = {
    'inside': 'country',
}

selector_index_map = {
    # Non-real selector indices, used for rule rewrites
    'arearule': -1,
    'closedrelation': -2,
}

mock_rules = {} # Contains the predicate selector part of mocked rules
def build_mock_rules():
    files = os.listdir(os.path.join(os.path.dirname(__file__), "mock_rules"))
    for f in list(map(lambda fn: fn[0:-7], files)):
        listener, tree = parse_mapcss("mapcss/mock_rules/" + f + ".mapcss")
        r = listener.stylesheet['rules'][0]['selectors'][0]['simple_selectors'][0]['predicates'][0]
        r['selector_index'] = None # Safety, for mock rules it should never propagate
        mock_rules.update({f: r})


def build_tests(tests):
    kv_split = re.compile('([^= ]*=)')
    out = []
    for test in tests:
        test_code = ""
        if test['context']:
            context = dict(map(lambda l: map(lambda s: s.strip(), l.split('=', 1)), test['context'].split(',')))
            context = dict(map(lambda kv: (context_map[kv[0]] if kv[0] in context_map else kv[0], kv[1]), context.items()))
            test_code = "with with_options(n, {%s}):\n    " % ', '.join(map(lambda kv: ": ".join(map(lambda s: "'" + s.replace("'", "\\'") + "'", kv)), context.items()))

        okvs = list(map(lambda s: s.strip(' ='), kv_split.split(test['what'][1:-1])))
        o, kvs = okvs[0], list(map(lambda a: a[0] in '"\'' and a[0] == a[-1] and a[1:-1] or a, map(lambda a: a.replace('\\\"', '"').replace("\\\'", "'"), okvs[1:])))
        kvs = zip(kvs[0::2], kvs[1::2]) # kvs.slice(2)
        tags = dict(kvs)
        test_code += ("self." + ("check_err" if test['type'].startswith('assertMatch') or test['type'].startswith('-osmoseAssertMatch') else "check_not_err") + "(" +
            "n." + o + "(data, {" + ', '.join(map(lambda kv: "'" + kv[0].replace("'", "\\'") + "': '" + kv[1].replace("'", "\\'") + "'", sorted(tags.items()))) + "}" + {'node': "", 'way': ", [0]", 'relation': ", []"}[o] + "), " +
            "expected={'class': " + str(test['class']) + ", 'subclass': " + str(test['subclass']) + "})")
        out.append(test_code)
    return "\n".join(out)

def parse_mapcss(inputfile):
    input = FileStream(inputfile, encoding='utf-8')
    lexer = MapCSSLexer(input)
    stream = CommonTokenStream(lexer)
    parser = MapCSSParser(stream)
    tree = parser.stylesheet()

    listener = MapCSSListenerL()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return listener, tree

def compile(inputfile, class_name, mapcss_url = None, only_for = [], not_for = [], prefix = ""):
    global item_default, class_map, subclass_blacklist, class_index, meta_tags

    listener, tree = parse_mapcss(inputfile)

    build_mock_rules()

    selectors_by_complexity = segregate_selectors_by_complexity(listener.stylesheet)
    if len(selectors_by_complexity['rules_complex']) > 0:
        print("W: Drop %d complex rules" % len(selectors_by_complexity['rules_complex']))
    tree = rewrite_tree(selectors_by_complexity['rules_meta'] + selectors_by_complexity['rules_simple'])
    tree = filter_non_productive_rules(tree)
    tree = filter_osmose_none_rules(tree)
    tree = filter_typeselector_rules(tree)
    tree = filter_support_rules(tree)
    selectors_type = segregate_selectors_type(tree)

    global class_, tests, regex_store, set_store
    rules = dict(map(lambda t: [t, to_p({'type': 'stylesheet', 'rules': selectors_type[t]})], sorted(selectors_type.keys(), key = lambda a: {'node': 0, 'way': 1, 'relation':2}[a])))
    items = build_items(class_)

    asserts = ""
    if tests:
        asserts = """

from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = """ + prefix + class_name + """(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        """ + build_tests(tests).replace("\n", "\n        ") + "\n"

    mapcss = ("""#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class """ + prefix + class_name + """(PluginMapCSS):
""" + ("\n    MAPCSS_URL = '" + mapcss_url + "'" if mapcss_url else "") + """
""" + ("\n    only_for = ['" + "', '".join(only_for) + "']\n" if only_for != [] else "") + """
""" + ("\n    not_for = ['" + "', '".join(not_for) + "']\n" if not_for != [] else "") + """
    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        """ + items.replace("\n", "\n        ") + """
        """ + "".join(map(lambda r: """
        self.""" + r[1] + " = re.compile(r'" + r[0].replace('(?U)', '').replace("'", "\\'") + "'" + (', ' + {'i': "re.I", 'm': "re.M", 's': "re.I"}[r[2]] if r[2] else '') + ")", map(lambda a: [a[0][0], a[1], a[0][1]], sorted(regex_store.items(), key = lambda s: s[1])))) + """

""" + "".join(map(lambda t: """
    def """ + t + """(self, data, tags""" + {'node': "", 'way': ", nds", 'relation': ", members"}[t] + """):
        capture_tags = {}
        keys = tags.keys()
        err = []
        """ + ((" = ".join(list(map(lambda s: "set_" + s, sorted(set_store)))) + " = False") if len(set_store) > 0 else "") + """

        """ + rules[t].replace("\n", "\n        ") + """
        return err
""", sorted(rules.keys(), key = lambda a: {'node': 0, 'way': 1, 'relation':2}[a])))
    + asserts).replace("        \n", "\n")
    return mapcss


from .item_map import item_map


def mapcss2osmose(mapcss, output_path = None):
    class_name = original_class_name = '.'.join(os.path.basename(mapcss).replace('.validator.', '.').split('.')[:-1])
    global item_default, class_map, subclass_blacklist, class_index, meta_tags
    if class_name in item_map:
        i = item_map[class_name]
        item_default = i.get('item')
        class_map = i.get('class') or {None: 0}
        subclass_blacklist = i.get('subclass_blacklist', [])
        mapcss_url = i.get('url_display', i.get('url'))
        only_for = i.get('only_for', [])
        not_for = i.get('not_for', [])
        prefix = i.get('prefix', '')
        class_index = max(class_map.values())
        meta_tags = ('["' + ('", "').join(i.get('tags')) + '"]') if i.get('tags') else None
    else:
        item_default = 0
        class_map = {}
        subclass_blacklist = []
        mapcss_url = None
        only_for = []
        not_for = []
        prefix = ''
        class_index = item_default * 1000
        meta_tags = None
    class_name = class_name.replace('.', '_').replace('-', '_')

    python_code = compile(mapcss, class_name, mapcss_url, only_for, not_for, prefix)

    path = output_path if output_path else os.path.dirname(mapcss)
    output = open((path or '.') + '/' + prefix + class_name + '.py', 'w')
    output.write(python_code)
    output.close()

    if original_class_name in item_map:
        item_map[original_class_name]['class'] = class_map
        f = open("mapcss/item_map.py", "w")
        f.write("#-*- coding: utf-8 -*-\n")
        f.write("item_map = \\\n")
        pprint(item_map, f)
        f.close()


if __name__ == '__main__':
    mapcss2osmose(mapcss = sys.argv[1])
