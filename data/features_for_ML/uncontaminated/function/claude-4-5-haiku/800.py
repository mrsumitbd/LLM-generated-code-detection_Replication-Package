def build_execution_tree(explain_result: str) -> ExecutionNode:
    '''
    Build a tree structure from result of df.explain("formatted").
    Parent - child relationship is established based on indentation level.
    Returns the root node of the tree.
    '''
    lines = explain_result.strip().split('\n')
    
    if not lines:
        return ExecutionNode("root")
    
    root = ExecutionNode("root")
    stack = [(root, -1)]
    
    for line in lines:
        if not line.strip():
            continue
        
        indent_level = len(line) - len(line.lstrip())
        content = line.strip()
        
        node = ExecutionNode(content)
        
        while len(stack) > 1 and stack[-1][1] >= indent_level:
            stack.pop()
        
        parent = stack[-1][0]
        parent.children.append(node)
        
        stack.append((node, indent_level))
    
    return root