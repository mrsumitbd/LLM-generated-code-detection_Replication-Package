def _get_name_node(ts_node: TSNode) -> TSNode | None:
    """Get the name node from a tree-sitter node."""
    if ts_node is None:
        return None
    
    # Check if the node itself is a name
    if ts_node.type in ('identifier', 'name'):
        return ts_node
    
    # Look for a child node that is a name
    for child in ts_node.children:
        if child.type in ('identifier', 'name'):
            return child
    
    # Check for common patterns where name is nested
    if ts_node.type in ('function_definition', 'class_definition', 'method_definition'):
        for child in ts_node.children:
            if child.type == 'identifier':
                return child
    
    return None