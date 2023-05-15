import subprocess
import os

from parser import Node, NodeType


def create_graphviz_string(node):
    graphviz_str = 'digraph G {\n'
    graphviz_str += create_node_string(node)
    graphviz_str += '}\n'
    return graphviz_str


def create_node_string(node, parent_id=''):
    node_id = get_unique_node_id()
    if isinstance(node, Node):
        node_str = f'  {node_id} [label="{node.node_type.value}"];\n'
    else:
        node_str = f'  {node_id} [label="{node}"];\n'
    if parent_id:
        node_str += f'  {parent_id} -> {node_id};\n'
    if isinstance(node, Node):
        for child in node.children:
            node_str += create_node_string(child, node_id)
    return node_str


def get_unique_node_id():
    get_unique_node_id.counter += 1
    return get_unique_node_id.counter


get_unique_node_id.counter = 0


def write_ast_dot(ast, output_file):
    output_file.write(create_graphviz_string(ast))


def save_ast_png(ast):
    with open('ast.dot', 'w') as f:
        write_ast_dot(ast, f)

    subprocess.run(['dot', '-Tpng', 'ast.dot', '-o', 'ast.png'])
    os.remove('ast.dot')


def print_ast(ast):
    def print_node(node, indent=0):
        if isinstance(node, list):
            for child in node:
                if isinstance(child, tuple):
                    print_node(child, indent)
                else:
                    print('    ' * indent + str(child))
        elif isinstance(node, tuple):
            if node[0] == 'function':
                if len(node) >= 5:
                    return_type, identifier, args, body = node[1:5]
                    print('    ' * indent + f'function {return_type} {identifier} {args}:')
                    print_node(body, indent + 1)
                else:
                    print('Invalid function node:', node)
            elif node[0] == 'assignment':
                if len(node) >= 3:
                    _, identifier, expression = node
                    print('    ' * indent + f'assignment {identifier}:')
                    print_node(expression, indent + 1)
                else:
                    print('Invalid assignment node:', node)
            elif node[0] == 'definition':
                if len(node) >= 4:
                    _, data_type, identifier, expression = node
                    print('    ' * indent + f'definition {data_type} {identifier}:')
                    print_node(expression, indent + 1)
                else:
                    print('Invalid definition node:', node)
            elif node[0] == 'expression':
                print('    ' * indent + 'expression:', node)
            else:
                print('    ' * indent + str(node[0]))
                print_node(node[1], indent + 1)
        else:
            print('    ' * indent + str(node))

    print_node(ast)
