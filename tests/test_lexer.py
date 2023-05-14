import pytest
from nihaoc.lexer import Lexer, TokenType


def test_lex_number():
    lexer = Lexer("123")
    tokens = lexer.lex()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == "123"

def test_lex_identifier():
    lexer = Lexer("variable")
    tokens = lexer.lex()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "variable"

def test_lex_string():
    lexer = Lexer('"Hello, world!"')
    tokens = lexer.lex()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "Hello, world!"

def test_lex_characters():
    lexer = Lexer("+-*/=")
    tokens = lexer.lex()
    assert len(tokens) == 5
    assert tokens[0].type == TokenType.CHARACTER
    assert tokens[0].value == "+"
    assert tokens[1].type == TokenType.CHARACTER
    assert tokens[1].value == "-"
    assert tokens[2].type == TokenType.CHARACTER
    assert tokens[2].value == "*"
    assert tokens[3].type == TokenType.CHARACTER
    assert tokens[3].value == "/"
    assert tokens[4].type == TokenType.CHARACTER
    assert tokens[4].value == "="

def test_lex_comments_and_whitespace():
    source_code = '''
    # This is a comment
    x = 10
    '''
    lexer = Lexer(source_code)
    tokens = lexer.lex()
    assert len(tokens) == 3
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "x"
    assert tokens[1].type == TokenType.CHARACTER
    assert tokens[1].value == "="
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == "10"

