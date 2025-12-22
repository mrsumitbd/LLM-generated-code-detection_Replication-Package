def build_execution_tree(explain_result: str) -> ExecutionNode:
    lines = explain_result.split('\n')
    
    def build_tree(lines, index):
        node = ExecutionNode(lines[index])
        while index + 1 < len(lines) and lines[index + 1].startswith(' '):
            child, index = build_tree(lines, index + 1)
            node.children.append(child)
        return node, index
    
    root = ExecutionNode(lines[0])
    index = 0
    while index + 1 < len(lines) and lines[index + 1].startswith(' '):
        child, index = build_tree(lines, index + 1)
        root.children.append(child)
    
    return root