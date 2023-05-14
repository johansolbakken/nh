import ply.lex as lex
from enum import Enum


class TokenType(Enum):
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    CHARACTER = 'CHARACTER'


tokens = [
    'NUMBER',
    'IDENTIFIER',
    'STRING',
    'CHARACTER'
]


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_CHARACTER(t):
    r'.'
    return t


t_ignore = ' \t'  # Ignore whitespace and tabs


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Invalid character: {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()
