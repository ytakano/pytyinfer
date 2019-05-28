import ply.lex as lex
import ply.yacc as yacc

# Grammar:
#
# VAR    := [a-zA-Z][a-zA-Z0-1]*
# TYPE   := : bool | : int | ∅
# LAMBDA := fun $VAR $TYPE { $LAMBDA }           |
#           if $LAMBDA then $LAMBDA else $LAMBDA |
#           $LAMBDA ( $LAMBDA )                  |
#           iszero ( $LAMBDA )                   |
#           pred ( $LAMBDA )                     |
#           succ ( $LAMBDA )                     |
#           true                                 |
#           false                                |
#           ( $LAMBDA )                          |
#           $VAR


# lexer

reserved = {
    'if'     : 'IF',
    'then'   : 'THEN',
    'else'   : 'ELSE',
    'succ'   : 'SUCC',
    'pred'   : 'PRED',
    'true'   : 'TRUE',
    'false'  : 'FALSE',
    'iszero' : 'ISZERO',
    'fun'    : 'FUN',
    'bool'   : 'BOOL',
    'int'    : 'INT',
}

tokens = [
    'ZERO',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'ID',
] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA  = r':'

t_ignore = ' \t'

def t_ZERO(t):
    r'0'
    t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(u"invalid character: '%s'" % t.value[0])


# parser

def p_expression_fun(p):
    'expression : FUN var LBRACE expression RBRACE'
    p[0] = ('lambda', p[2], p[4])

def p_expression_apply(p):
    'expression : expression LPAREN expression RPAREN'
    p[0] = ('apply', p[1], p[3])

def p_expression_if(p):
    'expression : IF expression THEN expression ELSE expression'
    p[0] = ('if', p[2], p[4], p[6])

def p_expression_true(p):
    'expression : TRUE'
    p[0] = 'true'

def p_expression_false(p):
    'expression : FALSE'
    p[0] = 'false'

def p_expression_zero(p):
    'expression : ZERO'
    p[0] = 'zero'

def p_expression_succ(p):
    'expression : SUCC LPAREN expression RPAREN'
    p[0] = ('succ', p[3])

def p_expression_pred(p):
    'expression : PRED LPAREN expression RPAREN'
    p[0] = ('pred', p[3])

def p_expression_iszero(p):
    'expression : ISZERO LPAREN expression RPAREN'
    p[0] = ('iszero', p[3])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_var(p):
    'expression : var'
    p[0] = p[1]

def p_var(p):
    'var : ID'
    p[0] = ('var', p[1])

if __name__ == '__main__':
    data = 'fun x { if x then succ(0) else succ(succ(0)) } (true)'
    lexer = lex.lex()
    parser = yacc.yacc()
    result = yacc.parse(data, lexer=lexer)
    print('expression:', data)
    print('AST:', result)
