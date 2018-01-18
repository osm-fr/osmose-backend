import sys
from antlr4 import *
from MapCSSLexer import MapCSSLexer
from MapCSSParser import MapCSSParser
from MapCSSListenerL import MapCSSListenerL


def to_mapcss(t):
    if isinstance(t, str):
        return t
    elif t['type'] == 'stylesheet':
        return "\n".join(map(to_mapcss, t['rules']))
    elif t['type'] == 'rule':
        return ",\n".join(map(to_mapcss, t['selectors'])) + " {\n    " + "\n    ".join(map(to_mapcss, t['declarations'])) + "\n}\n"
    elif t['type'] == 'selector':
        if t['operator']:
            return (
                to_mapcss(t['simple_selectors'][0]) + " " +
                t['operator'] +
                "".join(map(to_mapcss, t['link_selectors'])) +
                "".join(map(to_mapcss, t['pseudo_class'])) + " " +
                to_mapcss(t['simple_selectors'][1])
            )
        else:
            return "".join(map(to_mapcss, t['simple_selectors']))
    elif t['type'] == 'link_selector':
        if t['role']:
            return "[role" + t['operator'] + to_mapcss(t['role']) + "]"
        else: # t['index']
            return "[index" + t['operator'] + to_mapcss(t['index']) + "]"
    elif t['type'] == 'simple_selector':
        return (
            to_mapcss(t['type_selector']) +
            to_mapcss(t['zoom_selector']) +
            "".join(map(to_mapcss, t['class_selectors'])) +
            "".join(map(lambda a: "[" + to_mapcss(a) + "]", t['predicates'])) +
            "".join(map(to_mapcss, t['pseudo_class']))
        )
    elif t['type'] == 'class_selector':
        return ("!" if t['not'] else "") + "." + t['class']
    elif t['type'] == 'predicate_simple':
        return ("!" if t['not'] else "") + to_mapcss(t['predicate']) + ("?" if t['question_mark'] else "")
    elif t['type'] == 'pseudo_class':
        return (
            ("!" if t['not_class'] else "") +
            ":" + t['pseudo_class']
        )
    elif t['type'] == 'declaration':
        if t['set']:
            return "set " + t['set'] + ";"
        else:
            return to_mapcss(t['property']) + ": " + to_mapcss(t['value']) + ";"
    elif t['type'] == 'single_value':
        return to_mapcss(t['value'])
    elif t['type'] == 'declaration_value_function':
        return t['name'] + "(" + ", ".join(map(to_mapcss, t['params'])) + ")"
    elif t['type'] == 'booleanExpression':
        if t['operator'] == '(':
            return "(" + to_mapcss(t['operands'][0]) + ")"
        elif t['operator'] == '!':
            return "!" + to_mapcss(t['operands'][0])
        elif not t['operator']:
            return to_mapcss(t['operands'][0])
        else:
            return to_mapcss(t['operands'][0]) + t['operator'] + to_mapcss(t['operands'][1])
    elif t['type'] == 'valueExpression':
        if t['operator'] == '(':
            return "(" + to_mapcss(t['operands'][0]) + ")"
        if not t['operator']:
            return to_mapcss(t['operands'][0])
        else:
            return to_mapcss(t['operands'][0]) + t['operator'] + to_mapcss(t['operands'][1])
    elif t['type'] == 'zoom_selector':
        return to_mapcss(t['value'])
    elif t['type'] == 'quoted':
        return t['value']
    elif t['type'] == 'osmtag':
        return t['value']
    elif t['type'] == 'regexExpression':
        return "/" + to_mapcss(t['value']) + "/"
    elif t['type'] == 'functionExpression':
        return t['name'] + "(" + ", ".join(map(to_mapcss, t['params'])) + ")"
    elif t['type'] == 'primaryExpression':
        return ("*" if t['derefered'] else "") + to_mapcss(t['value'])
    else:
        return "<UNKNOW TYPE {0}>".format(t['type'])


def main(argv):
    input = FileStream(argv[1], encoding='utf-8')
    lexer = MapCSSLexer(input)
    stream = CommonTokenStream(lexer)
    parser = MapCSSParser(stream)
    tree = parser.stylesheet()

    listener = MapCSSListenerL()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    print(to_mapcss(listener.stylesheet))


if __name__ == '__main__':
    main(sys.argv)
