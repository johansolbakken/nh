def simplify_ast(ast):
    if isinstance(ast, list):
        return [simplify_ast(node) for node in ast]
    elif isinstance(ast, tuple):
        if ast[0] == 'function':
            return_type, identifier, args, body = ast[1:]
            return ('function', return_type, identifier, args, simplify_ast(body))
        elif ast[0] == 'print':
            expression = ast[1]
            return ('print', simplify_ast(expression))
        elif ast[0] == 'assignment':
            _, _, identifier, expression = ast
            return ('assignment', identifier, simplify_ast(expression))
        elif ast[0] == 'definition':
            _, data_type, identifier, expression = ast
            return ('definition', data_type, identifier, simplify_ast(expression))
        else:
            return (ast[0], simplify_ast(ast[1]))
    else:
        return ast
