import lexer

if __name__ == "__main__":
    source_code = '''
    # This is a comment
    x = 10
    y = "Hello, world!"
    print(x + y)
    '''

    lexer_instance = lexer.lexer
    lexer_instance.input(source_code)
    for token in lexer_instance:
        print(f'Type: {token.type}, Value: {token.value}, Line: {token.lineno}, Column: {token.lexpos + 1}')
