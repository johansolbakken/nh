import ply.yacc as yacc
from lexer import tokens, lexer

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH'),
    ('right', 'UMINUS'),
)


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
    '''GLOBAL : FUNCTION '''
    p[0] = p[1]


def p_FUNCTION(p):
    '''FUNCTION : RETURN_TYPE IDENTIFIER L_PAREN ARGUMENT_LIST R_PAREN STATEMENT
                | RETURN_TYPE IDENTIFIER L_PAREN R_PAREN STATEMENT'''
    if len(p) == 8:
        p[0] = ('function', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('function', p[1], p[2], [], p[5])


def p_STATEMENT(p):
    '''STATEMENT : BLOCK
                 | ASSIGNMENT_STATEMENT SEMICOLON
                 | DEFINITION_STATEMENT SEMICOLON
                 | FUNCTION_CALL SEMICOLON'''
    p[0] = p[1]


def p_ASSIGNMENT_STATEMENT(p):
    '''ASSIGNMENT_STATEMENT : IDENTIFIER EQUALS EXPRESSION'''
    p[0] = ('assignment', p[1], p[3])


def p_DEFINITION_STATEMENT(p):
    '''DEFINITION_STATEMENT : TYPE IDENTIFIER EQUALS EXPRESSION'''
    p[0] = ('definition', p[1], p[2], p[4])


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
                  | STRING_DATA
                  | FUNCTION_CALL
                  | EXPRESSION PLUS EXPRESSION
                  | EXPRESSION MINUS EXPRESSION
                  | EXPRESSION STAR EXPRESSION
                  | EXPRESSION SLASH EXPRESSION
                  | MINUS EXPRESSION %prec UMINUS'''
    if len(p) == 2:  # NUMBER, IDENTIFIER, STRING_DATA, FUNCTION_CALL
        p[0] = ('expression', p[1])
    elif len(p) == 3:  # MINUS EXPRESSION
        p[0] = ('expression', 'minus', p[2])
    else:  # EXPRESSION PLUS/MINUS/STAR/SLASH EXPRESSION
        p[0] = ('expression', p[2], p[1], p[3])


def p_EXPRESSION_LIST(p):
    '''EXPRESSION_LIST : EXPRESSION_LIST ',' EXPRESSION
                       | EXPRESSION'''
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_FUNCTION_CALL(p):
    '''FUNCTION_CALL : IDENTIFIER L_PAREN EXPRESSION_LIST R_PAREN
                    | IDENTIFIER L_PAREN R_PAREN'''
    if len(p) > 4:
        p[0] = ('function_call', p[1], p[3])
    else:
        p[0] = ('function_call', p[1], [])


def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token {p.value}")
    else:
        print("Syntax error: Unexpected end of input")


parser = yacc.yacc()


def parse(source_code):
    return parser.parse(source_code, lexer=lexer)
