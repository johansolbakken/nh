from parser import Node, NodeType, create_node


def simplify_ast(node: Node):
    for i, child in enumerate(node.children):
        if isinstance(child, Node):
            node.children[i] = simplify_ast(child)

    if node.node_type == NodeType.PROGRAM:
        return node.children[0]

    if node.node_type in [NodeType.GLOBAL, NodeType.RETURN_VALUE]:
        if len(node.children) == 1:
            return node.children[0]

    if node.node_type == NodeType.ARGUMENT:
        node.children = node.children[0].children
        return node

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

    if node.node_type in [NodeType.STATEMENT_LIST, NodeType.EXPRESSION_LIST, NodeType.ARGUMENT_LIST,
                          NodeType.GLOBAL_LIST, NodeType.STRUCT_MEMBER_LIST]:
        if len(node.children) == 2:
            if node.children[0].node_type in [NodeType.STATEMENT_LIST, NodeType.EXPRESSION_LIST, NodeType.ARGUMENT_LIST,
                                              NodeType.GLOBAL_LIST, NodeType.STRUCT_MEMBER_LIST]:
                node.children[0].children.append(node.children[1])
                return node.children[0]

    if node.node_type == NodeType.EXPRESSION:
        if len(node.children) == 1:
            return node.children[0]
        if len(node.children) == 3:
            if isinstance(node.children[0], Node) and isinstance(node.children[1], Node) and node.children[0].node_type == NodeType.NUMBER and node.children[2].node_type == NodeType.NUMBER:
                if node.children[1] == "+":
                    return create_node(NodeType.NUMBER, [node.children[0].children[0] + node.children[2].children[0]])
                if node.children[1] == "-":
                    return create_node(NodeType.NUMBER, [node.children[0].children[0] - node.children[2].children[0]])
                if node.children[1] == "*":
                    return create_node(NodeType.NUMBER, [node.children[0].children[0] * node.children[2].children[0]])
                if node.children[1] == "/":
                    return create_node(NodeType.NUMBER, [node.children[0].children[0] / node.children[2].children[0]])

    if node.node_type in [NodeType.EXPRESSION_LIST, NodeType.STATEMENT_LIST, NodeType.ARGUMENT_LIST,
                          NodeType.GLOBAL_LIST]:
        if len(node.children) == 1:
            return node.children[0]

    if node.node_type == NodeType.PARAMETER_LIST:
        if len(node.children) == 1 and node.children[0].node_type == NodeType.EXPRESSION_LIST:
            node.children = node.children[0].children
            return node

    if node.node_type == NodeType.STRUCT_MEMBER:
        return node.children[0]

    if node.node_type == NodeType.STRUCT_BODY:
        if len(node.children) == 1:
            return node.children[0]


    return node
