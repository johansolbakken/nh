import ply.yacc as yacc
from lexer import tokens, lexer


def p_expression(p):
    '''expression : NUMBER
                  | IDENTIFIER
                  | STRING
                  | CHARACTER'''
    p[0] = p[1]


def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token {p.value}")
    else:
        print("Syntax error: Unexpected end of input")


parser = yacc.yacc()


def parse(source_code):
    return parser.parse(source_code, lexer=lexer)
