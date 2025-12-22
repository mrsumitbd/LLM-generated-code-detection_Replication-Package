def find_first_child_by_field_name(node: TSNode, field_name: str) -> TSNode | None:
    for child in node.children:
        if child.field_name == field_name:
            return child
    return None