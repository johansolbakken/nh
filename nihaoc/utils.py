def print_ast(ast, indent=0):
    if isinstance(ast, list):
        for node in ast:
            print_ast(node, indent)
    elif isinstance(ast, tuple):
        if ast[0] == 'function':
            return_type, identifier, args, body = ast[1:]
            print(' ' * indent + f'function {return_type} {identifier} {args}:')
            print_ast(body, indent + 2)
        elif ast[0] == 'print':
            expression = ast[1]
            print(' ' * indent + 'print:')
            print_ast(expression, indent + 2)
        elif ast[0] == 'assignment':
            _, _, identifier, expression = ast
            print(' ' * indent + f'assignment {identifier}:')
            print_ast(expression, indent + 2)
        elif ast[0] == 'definition':
            _, data_type, identifier, expression = ast
            print(' ' * indent + f'definition {data_type} {identifier}:')
            print_ast(expression, indent + 2)
        else:
            print(' ' * indent + ast[0])
            print_ast(ast[1], indent + 2)
    else:
        print(' ' * indent + str(ast))
