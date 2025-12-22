def _get_name_node(ts_node: TSNode) -> TSNode | None:
    if ts_node.type == 'name':
        return ts_node
    for child in ts_node.children:
        result = _get_name_node(child)
        if result:
            return result
    return None