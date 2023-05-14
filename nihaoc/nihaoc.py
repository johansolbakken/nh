from lexer import Lexer

if __name__ == "__main__":
    source_code = '''
    # This is a comment
    x = 10
    y = "Hello, world!"
    print(x + y)
    '''

    scanner = Lexer(source_code)
    tokens = scanner.lex()

    for token in tokens:
        print(f'Type: {token.type.value}, Value: {token.value}, Line: {token.line}, Column: {token.column}')
