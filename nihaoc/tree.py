from parser import Node, NodeType, create_node


def simplify_ast(node: Node):
    for i, child in enumerate(node.children):
        if isinstance(child, Node):
            node.children[i] = simplify_ast(child)

    if node.node_type == NodeType.RETURN_TYPE:
        if isinstance(node.children[0], Node):
            node.children = node.children[0].children

    if node.node_type == NodeType.FUNC_ARG_LIST:
        if len(node.children) == 1:
            return node.children[0]
        else:
            return create_node(NodeType.ARGUMENT_LIST, node.children)

    return node
