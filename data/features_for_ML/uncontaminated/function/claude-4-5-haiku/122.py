def _recurse(node: Any):
    if isinstance(node, dict):
        return {k: _recurse(v) for k, v in node.items()}
    elif isinstance(node, list):
        return [_recurse(item) for item in node]
    elif isinstance(node, tuple):
        return tuple(_recurse(item) for item in node)
    else:
        return node