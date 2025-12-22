from tree_sitter import Node as TSNode

def find_first_child_by_field_name(node: TSNode, field_name: str) -> TSNode | None:
    child = node.child_by_field_name(field_name)
    if child is not None:
        return child
    for child in node.children:
        first_descendant = find_first_child_by_field_name(child, field_name)
        if first_descendant is not None:
            return first_descendant
    return None