from enum import Enum
from typing import List, Optional


class TokenType(Enum):
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    CHARACTER = 'CHARACTER'


class Token:
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type: TokenType = token_type
        self.value: str = value
        self.line: int = line
        self.column: int = column


class Lexer:
    def __init__(self, source_code: str):
        self.source_code: str = source_code
        self.pos: int = 0
        self.current_char: Optional[str] = self.source_code[self.pos]
        self.line: int = 1
        self.column: int = 1

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.source_code):
            self.current_char = self.source_code[self.pos]
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        else:
            self.current_char = None

    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def lex_number(self) -> Token:
        result: str = ''
        line: int = self.line
        column: int = self.column
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            line = self.line
            column = self.column
            self.advance()
        return Token(TokenType.NUMBER, result, line, column)

    def lex_identifier(self) -> Token:
        result: str = ''
        line: int = self.line
        column: int = self.column
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            line = self.line
            column = self.column
            self.advance()
        return Token(TokenType.IDENTIFIER, result, line, column)

    def lex_string(self) -> Token:
        result: str = ''
        line: int = self.line
        column: int = self.column
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            line = self.line
            column = self.column
            self.advance()
        self.advance()
        return Token(TokenType.STRING, result, line, column)

    def lex(self) -> List[Token]:
        tokens: List[Token] = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            elif self.current_char.isdigit():
                tokens.append(self.lex_number())
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.lex_identifier())
            elif self.current_char == '"':
                tokens.append(self.lex_string())
            elif self.current_char == '#':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
            else:
                tokens.append(Token(TokenType.CHARACTER, self.current_char, self.line, self.column))
                self.advance()
        return tokens
