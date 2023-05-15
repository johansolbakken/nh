from parser import Node, NodeType, create_node


def simplify_ast(node: Node):
    for i, child in enumerate(node.children):
        if isinstance(child, Node):
            node.children[i] = simplify_ast(child)

    if node.node_type == NodeType.PROGRAM:
        return node.children[0]

    if node.node_type == NodeType.RETURN_TYPE:
        if isinstance(node.children[0], Node):
            node.children = node.children[0].children

    if node.node_type == NodeType.FUNC_ARG_LIST:
        if len(node.children) == 1:
            return node.children[0]
        else:
            return create_node(NodeType.ARGUMENT_LIST, node.children)

    if node.node_type == NodeType.STATEMENT:
        return node.children[0]

    if node.node_type == NodeType.ARGUMENT_LIST:
        if len(node.children) == 1:
            return node.children[0]

    if node.node_type in [NodeType.STATEMENT_LIST, NodeType.GLOBAL_LIST]:
        if len(node.children) == 1:
            return node.children[0]

    if node.node_type == NodeType.EXPRESSION_LIST:
        if len(node.children) == 1:
            return node.children[0]

    if node.node_type == NodeType.EXPRESSION:
        if len(node.children) == 1:
            return node.children[0]

    return node
