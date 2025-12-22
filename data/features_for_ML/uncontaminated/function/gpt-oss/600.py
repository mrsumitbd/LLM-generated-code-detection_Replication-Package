def _get_name_node(ts_node: TSNode) -> TSNode | None:
    """
    Return the TSNode that represents the name of the given node, if any.
    This function attempts to locate an identifier node that serves as the
    name for declarations such as functions, classes, variables, etc.
    """
    # If the node itself is an identifier, return it.
    if getattr(ts_node, "type", None) == "identifier":
        return ts_node

    # Many tree-sitter nodes expose a 'name' field for the identifier.
    try:
        name_node = ts_node.child_by_field_name("name")
        if name_node is not None:
            return name_node
    except AttributeError:
        pass

    # Fallback: look for a named child that is an identifier.
    try:
        for child in ts_node.named_children:
            if getattr(child, "type", None) == "identifier":
                return child
    except AttributeError:
        pass

    # No name node found.
    return None