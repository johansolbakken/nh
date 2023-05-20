from typing import TextIO

from parser import Node, NodeType


def generate_member_access(f: TextIO, node: Node):
    f.write(f"{node.children[0].children[0]}.{node.children[1].children[0]}")


def generate_struct_member(f: TextIO, node: Node):
    type, name = node.children
    if type.children[0] == "int":
        f.write(f"        self.{name.children[0]} = 0\n")
    elif type.children[0] == "string":
        f.write(f"        self.{name.children[0]} = \"\"\n")


def generate_struct(f: TextIO, node: Node):
    name, member_list = node.children
    f.write(f"class {name.children[0]}:\n")
    f.write(f"    def __init__(self):\n")
    for member in member_list.children:
        generate_struct_member(f, member)
    f.write("\n")


def generate_expression(f: TextIO, node: Node):
    if node.node_type == NodeType.NUMBER:
        f.write(f"{node.children[0]}")
    elif node.node_type == NodeType.STRING:
        f.write(f'"{node.children[0]}"')
    elif node.node_type == NodeType.IDENTIFIER:
        f.write(f"{node.children[0]}")
    elif node.node_type == NodeType.FUNCTION_CALL:
        generate_function_call(f, node)
    elif node.node_type == NodeType.MEMBER_ACCESS:
        generate_member_access(f, node)
    elif len(node.children) == 1:
        generate_expression(f, node.children[0])
    elif len(node.children) == 2:
        f.write(f"-")
        generate_expression(f, node.children[1])
    elif len(node.children) == 3:
        generate_expression(f, node.children[0])
        f.write(f" {node.children[1]} ")
        generate_expression(f, node.children[2])
    elif len(node.children) == 0:
        pass
    else:
        print(node.children)
        raise Exception(f"Unknown expression type {node.node_type}")


def generate_assignment(f: TextIO, node: Node):
    name, expression = node.children
    if node.children[0].node_type == NodeType.MEMBER_ACCESS:
        generate_member_access(f, node.children[0])
    else:
        f.write(f"{name.children[0]}")
    f.write(" = ")
    generate_expression(f, expression)
    f.write("\n")


def generate_function_call(f: TextIO, node: Node):
    name, arg_list = node.children
    f.write(f"{name.children[0]}(")
    if arg_list.children:
        for arg in arg_list.children:
            if arg.node_type == NodeType.IDENTIFIER:
                f.write(f"{arg.children[0]}")
            elif arg.node_type == NodeType.NUMBER:
                f.write(f"{arg.children[0]}")
            elif arg.node_type == NodeType.STRING:
                f.write(f'"{arg.children[0]}"')
            else:
                generate_expression(f, arg)
            f.write(", ")
        f.seek(f.tell() - 2)
    f.write(")")


def generate_return(f: TextIO, node: Node):
    f.write("return ")
    generate_expression(f, node.children[0])
    f.write("\n")


def generate_definition(f: TextIO, node: Node):
    name, expression = node.children
    f.write(f"{name.children[1].children[0]} = ")
    generate_expression(f, expression)
    f.write("\n")


def generate_statement(f: TextIO, node: Node, indent: int = 4):
    if node.node_type == NodeType.ASSIGNMENT_STATEMENT:
        f.write(" " * indent)
        generate_assignment(f, node)
    elif node.node_type == NodeType.FUNCTION_CALL:
        f.write(" " * indent)
        generate_function_call(f, node)
        f.write("\n")
    elif node.node_type == NodeType.RETURN_STATEMENT:
        f.write(" " * indent)
        generate_return(f, node)
    elif node.node_type == NodeType.STATEMENT_LIST:
        for child in node.children:
            generate_statement(f, child, indent)
    elif node.node_type == NodeType.BLOCK:
        generate_statement(f, node.children[0])
    elif node.node_type == NodeType.DEFINITION_STATEMENT:
        f.write(" " * indent)
        generate_definition(f, node)
    else:
        raise Exception(f"Unknown statement type {node.node_type}")


def generate_function(f: TextIO, node: Node):
    return_type, name, arg_list, statement_list = node.children
    f.write(f"def {name.children[0]}(")
    if arg_list.node_type == NodeType.ARGUMENT:
        f.write(f"{arg_list.children[1].children[0]}")
    elif arg_list.children:
        for arg in arg_list.children:
            f.write(f"{arg.children[1].children[0]}, ")
        f.seek(f.tell() - 2)
    f.write("):\n")
    for statement in statement_list.children:
        generate_statement(f, statement, 4)
    f.write("\n")


def generate_globals(f: TextIO, node: Node):
    if node.node_type == NodeType.FUNCTION:
        generate_function(f, node)
    elif node.node_type == NodeType.STRUCT_DEFINITION:
        generate_struct(f, node)
    else:
        for child in node.children:
            if isinstance(child, Node):
                generate_globals(f, child)


def generate(node: Node, filename: str):
    with open(filename, "w") as f:
        generate_globals(f, node)
        f.write("\n")
        f.write("if __name__ == \"__main__\":\n")
        f.write("    main()\n")
