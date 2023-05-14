def simplify_ast(ast):
    if isinstance(ast, list):
        for i in range(len(ast)):
            ast[i] = simplify_ast(ast[i])
    if ast[0] == "function":
        ast = list(ast)
        ast[4] = simplify_ast(ast[4])
        ast = tuple(ast)
    elif ast[0] == "assignment":
        ast = list(ast)
        ast[2] = simplify_ast(ast[2])
        ast = tuple(ast)
    elif ast[0] == "expression":
        if len(ast) == 2:
            return ast[1]
        if ast[1] in ("+", "-", "*", "/"):
            ast = list(ast)
            ast[2] = simplify_ast(ast[2])
            ast[3] = simplify_ast(ast[3])
            if isinstance(ast[2], (int, float)) and isinstance(ast[3], (int, float)):
                if ast[1] == "+":
                    return ast[2] + ast[3]
                elif ast[1] == "-":
                    return ast[2] - ast[3]
                elif ast[1] == "*":
                    return ast[2] * ast[3]
                elif ast[1] == "/":
                    return ast[2] / ast[3]
            ast = tuple(ast)
        if ast[1] == "minus":
            ast = list(ast)
            ast[2] = simplify_ast(ast[2])
            if isinstance(ast[2], (int, float)):
                return -ast[2]
            ast = tuple(ast)
    return ast
