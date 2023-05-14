import parser

if __name__ == "__main__":
    source_code = '''
        # This is a comment
        x = 10
        y = "Hello, world!"
        print(x + y)
        '''

    result = parser.parse(source_code)
    print(result)
