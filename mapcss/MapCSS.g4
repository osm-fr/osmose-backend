grammar MapCSS;
/*
 * File originally based on https://github.com/Gubaer/dart-mapcss/blob/master/grammar/MapCSS.g
 * GPL 3.0 by Gubaer
 */

tokens {
   STYLESHEET,
   RULE,
   SIMPLE_SELECTOR,
   DESCENDANT_COMBINATOR,
   CHILD_COMBINATOR,
   PARENT_COMBINATOR,
   TYPE_SELECTOR,              // .text is the type
   ZOOM_SELECTOR,
   ATTRIBUTE_SELECTOR,
   CLASS_SELECTOR,
   ROLE_SELECTOR,
   INDEX_SELECTOR,
   PSEUDO_CLASS_SELECTOR,
   LAYER_ID_SELECTOR,         // .text is the layer id
   DECLARATION_BLOCK,
   DECLARATION,

   VALUE_RGB,
   VALUE_RGBA,
   VALUE_URL,
   VALUE_KEYWORD,              // .text is the keyword, without quotes
   VALUE_QUOTED,               // .text is the value (without quotes)
   VALUE_FLOAT,                // .text is the float value
   VALUE_INT,                  // .text is the int value
   VALUE_PERCENTAGE,           // .text is a float or int, *with* trailing %
   VALUE_POINTS,               // .text is a float or int, *with* trailing 'pt'
   VALUE_PIXELS,               // .text is a float or int, *with* trailing 'px'
   VALUE_LIST,
   VALUE_REGEXP,               // .text is a regular expression
   VALUE_INCREMENT,            // .text is the increment

   FUNCTION_CALL,
   PREDICATE,
   TR_CALL,
   EVAL_CALL
}

fragment EBACKSLASH: '\\\\';
fragment UNICODE: '\u0080'..'\uFFFD';  /* FIXME, Should be '\u0080'..'\uFFFE', but bug in antlr4 4.7, waiting for next release. */


COMMA: ',';
QUESTION_MARK: '?';
OP_INCLUDED_IN: '∈';
OP_INTERSECTS: '⧉';
PAR_OPEN: '(';
PAR_CLOSE: ')';
DOT: '.';

OP_EQ: '=';
OP_NEQ: '!=';
OP_LE: '<=';
OP_GE: '>=';
OP_LT: '<';
OP_GT: '>';
OP_MATCH: '=~';
OP_NOT_MATCH: '!~';
OP_STARTS_WITH: '^=';
OP_ENDS_WITH: '$=';
OP_SUBSTRING: '*=';
OP_CONTAINS: '~=';
OP_OR: '||';
OP_AND: '&&';
OP_MUL: '*';
OP_DIV: '/';
OP_MOD: '%';
OP_PLUS: '+';
OP_MINUS: '-';
OP_NOT: '!'; // NOTE: boolean not -> !(expr)

META: ('m' | 'M') ('e' | 'E') ('t' | 'T') ('a' | 'A');
SET: ('s' | 'S') ('e' | 'E') ('t' | 'T');
ROLE: ('r' | 'R') ('o' | 'O') ('l' | 'L') ('e' | 'E');
INDEX: ('i' | 'I') ('n' | 'N') ('d' | 'D') ('e' | 'E') ('x' | 'X');
IMPORT: '@' ('i' | 'I') ('m' | 'M') ('p' | 'P') ('o' | 'O')('r' | 'R') ('t' | 'T');


fragment DIGIT:  '0'..'9';
fragment CHAR: 'a'..'z' | 'A'..'Z';


/* Basic character sets from CSS specification */
fragment NONASCII: ~('\u0000' .. '\u009F');
fragment NMSTART: 'a'..'z' | 'A'..'Z' | '_' | NONASCII;
fragment NMCHAR: 'a'..'z' | 'A'..'Z' | '_' | '-' | NONASCII;

/* helpers */
NCOMPONENT: (CHAR | '_') (CHAR | DIGIT | '_' | '-')*;

LBRACKET: '[';
RBRACKET: ']';
LBRACE: '{';
RBRACE: '}';
COLON: ':';
SEMICOLON: ';';


/* -------------------- quoted strings -----------------------------------------------------------*/
fragment EDQUOTE: '\\"';
fragment ESQUOTE: '\\\'';
DQUOTED_STRING: '"' (' ' | '!' | '#'..'[' | ']'..'~' | '°' | UNICODE | EDQUOTE | EBACKSLASH)* '"';
SQUOTED_STRING: '\'' (' '..'&' | '('..'[' | ']'..'~' | '°' | UNICODE | ESQUOTE | EBACKSLASH)* '\'';

POSITIVE_INT: [0-9]+;
NEGATIVE_INT: '-' POSITIVE_INT;

POSITIVE_FLOAT: [0-9]+ | [0-9]* '.' [0-9]+;
NEGATIVE_FLOAT: '-' POSITIVE_FLOAT;

/* ----------------------------------------------------------------------------------------------- */
/* Zoom range                                                                                      */
/* ----------------------------------------------------------------------------------------------- */
RANGE: '|z' ('-' DIGIT+ | DIGIT+ ('-' (DIGIT+)?)? );

/* ----------------------------------------------------------------------------------------------- */
/* Regular expressions  and the '/' operator                                                       */
/* ----------------------------------------------------------------------------------------------- */
fragment REGEX_ESCAPE:   '\\/';
fragment REGEX_START: REGEX_ESCAPE | ' '..')' | '+'..'.' |'0'..'[' | ']'..'~' | '°' | '\\' | UNICODE;
fragment REGEX_CHAR:  REGEX_ESCAPE | ' '..'.' |'0'..'[' | ']'..'~' | '°' | '\\' | UNICODE;

REGEXP: '/' REGEX_START REGEX_CHAR* '/';


/* ----------------------------------------------------------------------------------------------- */
/* Whitespace and comments                                                                         */
/* ----------------------------------------------------------------------------------------------- */
WS:           (' ' | '\t' | '\n' | '\r' | '\f') -> channel(HIDDEN);
SL_COMMENT:   '//' .*? '\r'? '\n' -> channel(HIDDEN);
ML_COMMENT:   '/*'  .*? '*/' -> channel(HIDDEN);


/* =============================================================================================== */
/* Grammar                                                                                         */
/* ===============================================================================================  */

stylesheet
    : entry* EOF
    ;

entry
    : rule_
/*    | import_statement*/
    ;

rule_
    : META declaration_block
    | selector (COMMA selector)* COMMA* declaration_block
    ;

selector
    : simple_selector
    | simple_selector simple_selector
    | simple_selector OP_GT (link_selector | pseudo_class_selector)* simple_selector
    | simple_selector simple_selector_operator simple_selector
    ;

simple_selector_operator : OP_LT | OP_INCLUDED_IN | OP_INTERSECTS;

link_selector
    : LBRACKET ROLE valueOperator valueExpression RBRACKET
    | LBRACKET INDEX numericOperator v=int_ RBRACKET
    ;

layer_id_selector
    : COLON COLON k=cssident
    ;

simple_selector
    : type_selector (zoom_selector | class_selector | attribute_selector | pseudo_class_selector)* layer_id_selector?
    ;

zoom_selector
    : RANGE
    ;

quoted
    : DQUOTED_STRING
    | SQUOTED_STRING
    ;

cssident
    : '-' ?  NCOMPONENT
    ;

osmtag
    : '-' ?  NCOMPONENT ((':'|'.') NCOMPONENT)*
    ;

attribute_selector
    : LBRACKET predicate RBRACKET
    ;

predicate
    : predicate_simple
    | booleanExpression
    ;

predicate_simple
    : OP_NOT ? (osmtag | quoted) QUESTION_MARK ?
    | OP_NOT ? regexExpression
    ;

class_selector
    : OP_NOT DOT cssident
    | DOT cssident
    ;

pseudo_class_selector
    : COLON OP_NOT cssident
    | OP_NOT COLON cssident
    | COLON cssident
    ;

type_selector
    : cssident
    | OP_MUL
    ;

declaration_block
    :  l=LBRACE declarations RBRACE
    |  l=LBRACE RBRACE
    ;

declarations
    : declaration (SEMICOLON declaration)* SEMICOLON*
    ;

declaration
    : SET DOT ? cssident
    | declaration_property COLON declaration_value
    ;

declaration_property
    : cssident
    ;

declaration_value
    : single_value
/*    | EVAL  PAR_OPEN expr PAR_CLOSE*/
    | declaration_value_function
    ;

declaration_value_function
    : cssident PAR_OPEN (declaration_value (COMMA declaration_value)*)? PAR_CLOSE
    ;

int_
    : n=POSITIVE_INT
    | n=NEGATIVE_INT
    ;

num
    : n=POSITIVE_INT
    | n=NEGATIVE_INT
    | n=POSITIVE_FLOAT
    | n=NEGATIVE_FLOAT
    ;

single_value
    : v=POSITIVE_INT
    | v=NEGATIVE_INT
    | v=POSITIVE_FLOAT
    | v=NEGATIVE_FLOAT
    | quoted
/*    | declaration_value_function*/
    /* make sure these are the last alternatives in this rule */
    | osmtag
    ;

/* ------------------------------------------------------------------------------------------ */
/* Expressions                                                                                */
/* ------------------------------------------------------------------------------------------ */
booleanOperator
    : OP_OR | OP_AND | OP_EQ | OP_NEQ
    ;

numericOperator
    : OP_EQ | OP_NEQ | OP_LT | OP_LE | OP_GT | OP_GE
    ;

valueOperator
    : numericOperator
    | OP_STARTS_WITH | OP_ENDS_WITH
    | OP_SUBSTRING | OP_CONTAINS
    ;

regexOperator
    : OP_MATCH | OP_NOT_MATCH
    ;

booleanExpression
    : op=PAR_OPEN booleanExpression PAR_CLOSE
    | op=OP_NOT booleanExpression
    | booleanExpression booleanOperator booleanExpression
    | valueExpression valueOperator valueExpression
    | valueExpression regexOperator regexExpression
    | functionExpression
    ;

valueExpression
    : op=PAR_OPEN valueExpression PAR_CLOSE
    | valueExpression op=(OP_PLUS | OP_MINUS | OP_MUL | OP_DIV | OP_MOD) valueExpression
    | primaryExpression
    | functionExpression
    ;

regexExpression
    : quoted
    | REGEXP
    ;

functionExpression
    : f=cssident PAR_OPEN (valueExpression (COMMA valueExpression)*)? PAR_CLOSE
    ;

primaryExpression
    : v=POSITIVE_FLOAT
    | v=POSITIVE_INT
    | v=NEGATIVE_FLOAT
    | v=NEGATIVE_INT
    | OP_MUL ? quoted
    | OP_MUL ? osmtag
    | OP_MUL regexExpression
    ;
