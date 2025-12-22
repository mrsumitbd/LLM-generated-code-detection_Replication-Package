def find_first_child_by_field_name(node: TSNode, field_name: str) -> TSNode | None:
    for child in node.children:
        if child.type == field_name:
            return child
    return None