def find_first_child_by_field_name(node: TSNode, field_name: str) -> TSNode | None:
    if node is None:
        return None
    
    for child in node.children:
        if child.field_name == field_name:
            return child
    
    for child in node.children:
        result = find_first_child_by_field_name(child, field_name)
        if result is not None:
            return result
    
    return None