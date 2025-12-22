def build_execution_tree(explain_result: str) -> ExecutionNode:
    '''
    Build a tree structure from result of df.explain("formatted").
    Parent - child relationship is established based on indentation level.
    Returns the root node of the tree.
    '''
    exec_plan, node_details = split_formatted_explain(explain_result)
    flat_nodes = parse_execution_plan(exec_plan)
    node_details_dict = parse_node_details(node_details)

    stack = []
    root = None

    for node in flat_nodes:
        node.set_properties(node_details_dict[node.id])
        while stack and stack[-1].height >= node.height:
            stack.pop()

        if stack:
            stack[-1].add_child(node)
        elif root:
            raise ValueError(f"Execution graph contains multiple roots: {root.name} and {node.name}")
        else:
            root = node

        stack.append(node)
    return root