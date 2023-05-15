from typing import Optional

import ply
import ply.yacc as yacc
from lexer import tokens, lexer
from enum import Enum


class NodeType(Enum):
    PROGRAM = 'PROGRAM'
    GLOBAL_LIST = 'GLOBAL_LIST'
    GLOBAL = 'GLOBAL'
    FUNCTION = 'FUNCTION'
    STATEMENT = 'STATEMENT'
    ASSIGNMENT_STATEMENT = 'ASSIGNMENT_STATEMENT'
    DEFINITION_STATEMENT = 'DEFINITION_STATEMENT'
    RETURN_STATEMENT = 'RETURN_STATEMENT'
    BLOCK = 'BLOCK'
    STATEMENT_LIST = 'STATEMENT_LIST'
    RETURN_TYPE = 'RETURN_TYPE'
    TYPE = 'TYPE'
    ARGUMENT_LIST = 'ARGUMENT_LIST'
    ARGUMENT = 'ARGUMENT'
    EXPRESSION = 'EXPRESSION'
    EXPRESSION_LIST = 'EXPRESSION_LIST'
    RETURN_VALUE = 'RETURN_VALUE'
    DEFINITION = 'DEFINITION'
    PARAMETER_LIST = 'PARAMETER_LIST'
    FUNCTION_CALL = 'FUNCTION_CALL'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    FUNC_ARG_LIST = 'FUNC_ARG_LIST'


class Node:
    def __init__(self, node_type: NodeType):
        self.node_type = node_type
        self.children = []
        self.token: Optional[ply.lex.LexToken] = None

    def to_string(self, indent=0):
        s = ""
        s += " " * indent + str(self.node_type) + "\n"
        for child in self.children:
            if isinstance(child, Node):
                s += child.to_string(indent + 4)
            elif child is not None:
                s += " " * (indent + 4) + str(child) + "\n"
        return s


def create_node(node_type: NodeType, children: list = None, token: Optional[ply.lex.LexToken] = None):
    node = Node(node_type)
    if children:
        node.children = children
    if token:
        node.token = token
    return node


precedence = (
    ('left', 'PLUS'),
    ('left', 'MINUS'),
    ('left', 'STAR'),
    ('left', 'SLASH'),
    ('right', 'UMINUS'),
)


def p_PROGRAM(p):
    '''PROGRAM : GLOBAL_LIST'''
    p[0] = create_node(NodeType.PROGRAM, [p[1]])


def p_GLOBAL_LIST(p):
    '''GLOBAL_LIST : GLOBAL_LIST GLOBAL
                   | GLOBAL'''
    if len(p) > 2:
        p[0] = create_node(NodeType.GLOBAL_LIST, [p[1], p[2]])
    else:
        p[0] = create_node(NodeType.GLOBAL_LIST, [p[1]])


def p_GLOBAL(p):
    '''GLOBAL : FUNCTION '''
    p[0] = create_node(NodeType.GLOBAL, [p[1]])


def p_FUNCTION(p):
    '''FUNCTION : RETURN_TYPE IDENTIFIER L_PAREN FUNC_ARG_LIST R_PAREN STATEMENT'''
    p[0] = create_node(NodeType.FUNCTION, [p[1], p[2], p[4], p[6]])


def p_FUNC_ARG_LIST(p):
    '''FUNC_ARG_LIST : ARGUMENT_LIST
                     | '''
    if len(p) > 1:
        p[0] = create_node(NodeType.FUNC_ARG_LIST, [p[1]])
    else:
        p[0] = create_node(NodeType.FUNC_ARG_LIST)


def p_STATEMENT(p):
    '''STATEMENT : BLOCK
                 | ASSIGNMENT_STATEMENT SEMICOLON
                 | DEFINITION_STATEMENT SEMICOLON
                 | FUNCTION_CALL SEMICOLON
                 | RETURN_STATEMENT SEMICOLON'''
    p[0] = create_node(NodeType.STATEMENT, [p[1]])


def p_ASSIGNMENT_STATEMENT(p):
    '''ASSIGNMENT_STATEMENT : IDENTIFIER EQUALS EXPRESSION'''
    p[0] = create_node(NodeType.ASSIGNMENT_STATEMENT, [p[1], p[3]])


def p_DEFINITION_STATEMENT(p):
    '''DEFINITION_STATEMENT : DEFINITION EQUALS EXPRESSION'''
    p[0] = create_node(NodeType.DEFINITION_STATEMENT, [p[1], p[3]])


def p_RETURN_STATEMENT(p):
    '''RETURN_STATEMENT : RETURN RETURN_VALUE'''
    p[0] = create_node(NodeType.RETURN_STATEMENT, [p[2]])


def p_RETURN_VALUE(p):
    '''RETURN_VALUE : EXPRESSION
                    |'''
    if len(p) > 1:
        p[0] = create_node(NodeType.RETURN_VALUE, [p[1]])
    else:
        p[0] = create_node(NodeType.RETURN_VALUE)


def p_BLOCK(p):
    '''BLOCK : L_BRACE STATEMENT_LIST R_BRACE'''
    p[0] = create_node(NodeType.BLOCK, [p[2]])


def p_STATEMENT_LIST(p):
    '''STATEMENT_LIST : STATEMENT_LIST STATEMENT
                      | STATEMENT'''
    if len(p) > 2:
        p[0] = create_node(NodeType.STATEMENT_LIST, [p[1], p[2]])
    else:
        p[0] = create_node(NodeType.STATEMENT_LIST, [p[1]])


def p_RETURN_TYPE(p):
    '''RETURN_TYPE : TYPE
                   | TYPE_VOID'''
    p[0] = create_node(NodeType.RETURN_TYPE, [p[1]])


def p_TYPE(p):
    '''TYPE : TYPE_INT
            | TYPE_FLOAT
            | TYPE_STRING'''
    p[0] = create_node(NodeType.TYPE, [p[1]])


def p_ARGUMENT_LIST(p):
    '''ARGUMENT_LIST : ARGUMENT_LIST COMMA ARGUMENT
                     | ARGUMENT'''
    if len(p) > 3:
        p[0] = create_node(NodeType.ARGUMENT_LIST, [p[1], p[3]])
    else:
        p[0] = create_node(NodeType.ARGUMENT_LIST, [p[1]])


def p_ARGUMENT(p):
    '''ARGUMENT : DEFINITION'''
    p[0] = create_node(NodeType.ARGUMENT, [p[1]])


def p_EXPRESSION(p):
    '''EXPRESSION : EXPRESSION PLUS EXPRESSION %prec PLUS
                  | EXPRESSION MINUS EXPRESSION %prec MINUS
                  | EXPRESSION STAR EXPRESSION %prec STAR
                  | EXPRESSION SLASH EXPRESSION %prec SLASH
                  | MINUS EXPRESSION %prec UMINUS
                  | L_PAREN EXPRESSION R_PAREN
                  | NUMBER
                  | IDENTIFIER
                  | STRING
                  | FUNCTION_CALL'''
    if len(p) == 4:
        if p[1] == '(' and p[3] == ')':
            p[0] = create_node(NodeType.EXPRESSION, [p[2]])
        else:
            p[0] = create_node(NodeType.EXPRESSION, [p[1], p[2], p[3]])
    elif len(p) == 3:
        p[0] = create_node(NodeType.EXPRESSION, [p[1], p[2]])
    else:
        p[0] = create_node(NodeType.EXPRESSION, [p[1]])

def p_DEFINITION(p):
    '''DEFINITION : TYPE IDENTIFIER'''
    p[0] = create_node(NodeType.DEFINITION, [p[1], p[2]])


def p_PARAMETER_LIST(p):
    '''PARAMETER_LIST : EXPRESSION_LIST
                      | '''
    if len(p) > 1:
        p[0] = create_node(NodeType.PARAMETER_LIST, [p[1]])
    else:
        p[0] = create_node(NodeType.PARAMETER_LIST)


def p_EXPRESSION_LIST(p):
    '''EXPRESSION_LIST : EXPRESSION_LIST COMMA EXPRESSION
                       | EXPRESSION'''
    if len(p) > 3:
        p[0] = create_node(NodeType.EXPRESSION_LIST, [p[1], p[3]])
    else:
        p[0] = create_node(NodeType.EXPRESSION_LIST, [p[1]])


def p_FUNCTION_CALL(p):
    '''FUNCTION_CALL : IDENTIFIER L_PAREN PARAMETER_LIST R_PAREN'''
    p[0] = create_node(NodeType.FUNCTION_CALL, [p[1], p[3]])


def p_IDENTIFIER(p):
    '''IDENTIFIER : IDENTIFIER_DATA'''
    p[0] = create_node(NodeType.IDENTIFIER, [p[1]])


def p_NUMBER(p):
    '''NUMBER : NUMBER_DATA'''
    p[0] = create_node(NodeType.NUMBER, [p[1]])


def p_STRING(p):
    '''STRING : STRING_DATA'''
    p[0] = create_node(NodeType.STRING, [p[1]])


def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token {p.value}")
    else:
        print("Syntax error: Unexpected end of input")


parser = yacc.yacc()


def parse(source_code):
    return parser.parse(source_code, lexer=lexer)
