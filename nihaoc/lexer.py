import ply.lex as lex
from enum import Enum


class TokenType(Enum):
    NUMBER_DATA = 'NUMBER'
    IDENTIFIER_DATA = 'IDENTIFIER'
    STRING_DATA = 'STRING_DATA'
    TYPE_VOID = 'TYPE_VOID'
    TYPE_STRING = 'TYPE_STRING'
    TYPE_INT = 'TYPE_INT'
    TYPE_FLOAT = 'TYPE_FLOAT'
    L_PAREN = 'L_PAREN'
    R_PAREN = 'R_PAREN'
    L_BRACE = 'L_BRACE'
    R_BRACE = 'R_BRACE'
    EQUALS = 'EQUALS'
    SEMICOLON = 'SEMICOLON'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    STAR = 'STAR'
    SLASH = 'SLASH'
    COMMA = 'COMMA'
    RETURN = 'RETURN'


tokens = [
    'NUMBER_DATA',
    'IDENTIFIER_DATA',
    'STRING_DATA',
    'TYPE_VOID',
    'TYPE_STRING',
    'TYPE_INT',
    'TYPE_FLOAT',
    'L_PAREN',
    'R_PAREN',
    'L_BRACE',
    'R_BRACE',
    'EQUALS',
    'SEMICOLON',
    'PLUS',
    'MINUS',
    'STAR',
    'SLASH',
    'COMMA',
    'RETURN'
]


def t_TYPE_VOID(t):
    r'void'
    t.type = TokenType.TYPE_VOID.value
    return t


def t_TYPE_STRING(t):
    r'string'
    t.type = TokenType.TYPE_STRING.value
    return t


def t_TYPE_INT(t):
    r'int'
    t.type = TokenType.TYPE_INT.value
    return t


def t_TYPE_FLOAT(t):
    r'float'
    t.type = TokenType.TYPE_FLOAT.value
    return t


def t_NUMBER_DATA(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_RETURN(t):
    r'return'
    t.type = TokenType.RETURN.value
    return t

def t_IDENTIFIER_DATA(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value
    return t


def t_STRING_DATA(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t



t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_BRACE = r'\{'
t_R_BRACE = r'\}'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_COMMA = r','

t_ignore = ' \t'  # Ignore whitespace and tabs


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Invalid character: {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()
