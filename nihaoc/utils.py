import subprocess
import os


def write_ast_dot(ast, output_file):
    def write_node(node, parent_id=None):
        node_id = str(id(node))
        output_file.write(f'    {node_id} [label="{node}"];\n')

        if parent_id is not None:
            output_file.write(f'    {parent_id} -> {node_id};\n')

        if isinstance(node, list):
            for child in node:
                if isinstance(child, tuple):
                    child_id = write_node(child, node_id)
                    output_file.write(f'    {node_id} -> {child_id};\n')
                else:
                    child_id = str(id(child))
                    output_file.write(f'    {child_id} [label="{child}"];\n')
                    output_file.write(f'    {node_id} -> {child_id};\n')

        elif isinstance(node, tuple):
            if node[0] == 'function':
                if len(node) >= 5:
                    return_type, identifier, args, body = node[1:5]
                    output_file.write(f'    {node_id} [label="function (function)"];\n')
                    output_file.write(f'    {node_id} -> {str(id(return_type))};\n')
                    output_file.write(f'    {node_id} -> {str(id(identifier))};\n')
                    output_file.write(f'    {node_id} -> {str(id(args))};\n')
                    output_file.write(f'    {node_id} -> {str(id(body))};\n')
                    write_node(return_type, str(id(return_type)))
                    write_node(identifier, str(id(identifier)))
                    write_node(args, str(id(args)))
                    write_node(body, str(id(body)))
                else:
                    output_file.write(f'    {node_id} [label="Invalid function node: {node}"];\n')

            elif node[0] == 'print':
                if len(node) >= 2:
                    expression = node[1]
                    output_file.write(f'    {node_id} [label="print (print)"];\n')
                    output_file.write(f'    {node_id} -> {str(id(expression))};\n')
                    write_node(expression, str(id(expression)))
                else:
                    output_file.write(f'    {node_id} [label="Invalid print node: {node}"];\n')

            elif node[0] == 'assignment':
                if len(node) >= 4:
                    _, _, identifier, expression = node
                    output_file.write(f'    {node_id} [label="assignment (assignment)"];\n')
                    output_file.write(f'    {node_id} -> {str(id(identifier))};\n')
                    output_file.write(f'    {node_id} -> {str(id(expression))};\n')
                    write_node(identifier, str(id(identifier)))
                    write_node(expression, str(id(expression)))
                else:
                    output_file.write(f'    {node_id} [label="Invalid assignment node: {node}"];\n')

            elif node[0] == 'definition':
                if len(node) >= 4:
                    _, data_type, identifier, expression = node
                    output_file.write(f'    {node_id} [label="definition (definition)"];\n')
                    output_file.write(f'    {node_id} -> {str(id(data_type))};\n')
                    output_file.write(f'    {node_id} -> {str(id(identifier))};\n')
                    output_file.write(f'    {node_id} -> {str(id(expression))};\n')
                    write_node(data_type, str(id(data_type)))
                    write_node(identifier, str(id(identifier)))
                    write_node(expression, str(id(expression)))
                else:
                    output_file.write(f' {node_id} [label="Invalid definition node: {node}"];\n')
            elif node[0] == 'expression':
                output_file.write(f'    {node_id} [label="expression (expression)"];\n')
                for i, child in enumerate(node[1:], start=1):
                    output_file.write(f'    {node_id} -> {str(id(child))};\n')
                    write_node(child, str(id(child)))

            else:
                output_file.write(f'    {node_id} [label="{node[0]}"];\n')
                output_file.write(f'    {node_id} -> {str(id(node[1]))};\n')
                write_node(node[1], str(id(node[1])))

        else:
            output_file.write(f'    {node_id} [label="{node}"];\n')

        return node_id

    output_file.write('digraph AST {\n')
    write_node(ast)
    output_file.write('}\n')


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

