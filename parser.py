import ply.lex as lex
import ply.yacc as yacc

# Grammar:
#
# VAR := [a-zA-Z][a-zA-Z0-1]*
# EXP := fun $VAR { $EXP }              |
#           if $EXP then $EXP else $EXP |
#           $EXP ( $EXP )               |
#           iszero ( $EXP )             |
#           pred ( $EXP )               |
#           succ ( $EXP )               |
#           true                        |
#           false                       |
#           ( $EXP )                    |
#           $VAR


# data which will be parsed
data = ''


# tokenizer

# reserved words
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
}

tokens = [
    'ZERO',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'ID',
] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_ignore = ' \t'

def t_ZERO(t):
    r'0'
    t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_error(t):
    print(u"invalid character: '%s'" % t.value[0])

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



# parser

# Compute column.
#   lexpos is the position of lexer
def find_column(lexpos):
    line_start = data.rfind('\n', 0, lexpos) + 1
    return (lexpos - line_start) + 1

# get the line and the column number of token p[n]
#   p is a parse context of ply
#   n is the position of the token in p
def get_pos(p, n):
    return {'line': p.lineno(n),
            'column': find_column(p.lexpos(n))}

def p_expression_fun(p):
    'expression : FUN var LBRACE expression RBRACE'
    p[0] = ['lambda', get_pos(p, 1), p[2], p[4]]

def p_expression_apply(p):
    'expression : expression LPAREN expression RPAREN'
    p[0] = ['apply', get_pos(p, 1), p[1], p[3]]

def p_expression_if(p):
    'expression : IF expression THEN expression ELSE expression'
    p[0] = ['if', get_pos(p, 1), p[2], p[4], p[6]]

def p_expression_true(p):
    'expression : TRUE'
    p[0] = ['true', get_pos(p, 1)]

def p_expression_false(p):
    'expression : FALSE'
    p[0] = ['false', get_pos(p, 1)]

def p_expression_zero(p):
    'expression : ZERO'
    p[0] = ['zero', get_pos(p, 1)]

def p_expression_succ(p):
    'expression : SUCC LPAREN expression RPAREN'
    p[0] = ['succ', get_pos(p, 1), p[3]]

def p_expression_pred(p):
    'expression : PRED LPAREN expression RPAREN'
    p[0] = ['pred', get_pos(p, 1), p[3]]

def p_expression_iszero(p):
    'expression : ISZERO LPAREN expression RPAREN'
    p[0] = ['iszero', get_pos(p, 1), p[3]]

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_var(p):
    'expression : var'
    p[0] = p[1]

def p_var(p):
    'var : ID'
    p[0] = ['var', get_pos(p, 1), p[1]]

def p_error(p):
    if p:
        print('Syntax error: %d:%d: %r' % (p.lineno, find_column(p.lexpos), p.value))
        exit()
    else:
        print('Syntax error: EOF')

def parse(s):
    data = s
    lexer = lex.lex()
    parser = yacc.yacc()
    return yacc.parse(data, lexer=lexer, tracking=True)
