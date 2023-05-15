def generate_expression(f, expression, indent):
    if expression[1] == "minus":
        f.write("-")
        generate_expression(f, expression[2], indent)
    elif expression[1] in ("+", "-", "*", "/"):
        f.write("(")
        generate_expression(f, expression[2], indent)
        f.write(f" {expression[1]} ")
        generate_expression(f, expression[3], indent)
        f.write(")")
    elif expression[0] == "identifier":
        f.write(expression[1])
    elif expression[0] == "number":
        f.write(str(expression[1]))
    elif expression[0] == "string":
        f.write(f'"{expression[1]}"')
    elif expression[0] == "expression":
        generate_expression(f, expression[1], indent)
    else:
        f.write(str(expression[1]))


def generate_return_type(f, return_type, indent):
    if return_type[0] == "type":
        f.write(return_type[1])
    else:
        f.write("void")


def generate_statement(f, statement, indent):
    if statement[0] == "assignment":
        f.write("    " * indent)
        f.write(f"{statement[1][1]} = ")
        generate_expression(f, statement[2], indent)
        f.write("\n")
    elif statement[0] == "declaration":
        f.write("    " * indent)
        f.write(f"{statement[2].name} = ")
        generate_expression(f, statement[3], indent)
        f.write("\n")
    elif statement[0] == "function_call":
        f.write("    " * indent)
        f.write(f"{statement[1][1]}(")
        for i, arg in enumerate(statement[2]):
            if i != 0:
                f.write(", ")
            generate_expression(f, arg, indent)
        f.write(")\n")
    elif statement[0] == "block":
        generate_statement(f, statement, indent + 1)
    elif statement[0] == "return":
        generate_return(f, statement, indent)


def generate_function(f, function):
    f.write(f"def {function[2][1]}(")
    for i, arg in enumerate(function[3]):
        if i != 0:
            f.write(", ")
        f.write(f"{arg.name}: {arg.data_type}")
    f.write("):\n")
    for statement in function[4]:
        generate_statement(f, statement, 1)


def generate(ast, filename):
    with open(filename, "w") as f:
        for function in ast:
            generate_function(f, function)
        f.write("\n")
        f.write("if __name__ == \"__main__\":\n")
        f.write("    main()\n")
