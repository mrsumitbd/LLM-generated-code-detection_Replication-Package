def _get_name_node(ts_node: TSNode) -> TSNode | None:
    if ts_node.type == 'identifier':
        return ts_node
    for child in ts_node.children:
        name_node = _get_name_node(child)
        if name_node is not None:
            return name_node
    return None