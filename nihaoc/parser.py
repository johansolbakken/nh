import ply.yacc as yacc
from lexer import tokens, lexer


def p_PROGRAM(p):
    '''PROGRAM : GLOBAL_LIST'''
    p[0] = p[1]


def p_GLOBAL_LIST(p):
    '''GLOBAL_LIST : GLOBAL_LIST GLOBAL
                   | GLOBAL'''
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_GLOBAL(p):
    '''GLOBAL : FUNCTION
              | STATEMENT'''
    p[0] = p[1]


def p_FUNCTION(p):
    '''FUNCTION : RETURN_TYPE IDENTIFIER L_PAREN ARGUMENT_LIST R_PAREN STATEMENT'''
    p[0] = ('function', p[1], p[2], p[4], p[6])


def p_STATEMENT(p):
    '''STATEMENT : BLOCK
                 | PRINT_STATEMENT'''
    p[0] = p[1]


def p_BLOCK(p):
    '''BLOCK : L_BRACE STATEMENT_LIST R_BRACE'''
    p[0] = p[2]


def p_STATEMENT_LIST(p):
    '''STATEMENT_LIST : STATEMENT_LIST STATEMENT
                      | STATEMENT'''
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_PRINT_STATEMENT(p):
    '''PRINT_STATEMENT : PRINT L_PAREN EXPRESSION R_PAREN'''
    p[0] = ('print', p[3])


def p_RETURN_TYPE(p):
    '''RETURN_TYPE : TYPE
                   | TYPE_VOID'''
    p[0] = p[1]


def p_TYPE(p):
    '''TYPE : TYPE_INT
            | TYPE_FLOAT
            | TYPE_STRING'''
    p[0] = p[1]


def p_ARGUMENT_LIST(p):
    '''ARGUMENT_LIST : ARGUMENT_LIST ',' IDENTIFIER
                     | IDENTIFIER'''
    if len(p) > 2:
        p[0] = [p[1]] + [p[3]]
    elif p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_EXPRESSION(p):
    '''EXPRESSION : NUMBER
                  | IDENTIFIER
                  | STRING_DATA'''
    p[0] = p[1]


def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token {p.value}")
    else:
        print("Syntax error: Unexpected end of input")


parser = yacc.yacc()


def parse(source_code):
    return parser.parse(source_code, lexer=lexer)
