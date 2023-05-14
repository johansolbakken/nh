import re

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0
        self.current_char = self.source_code[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.source_code):
            self.current_char = self.source_code[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def lex_number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token('NUMBER', result)

    def lex_identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum() or self.current_char == '_':
            result += self.current_char
            self.advance()
        return Token('IDENTIFIER', result)

    def lex_string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()
        return Token('STRING', result)

    def lex(self):
        tokens = []
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
                tokens.append(Token('CHARACTER', self.current_char))
                self.advance()
        return tokens