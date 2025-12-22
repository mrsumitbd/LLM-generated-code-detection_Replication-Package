def _recurse(node: Any):
    if isinstance(node, list):
        for item in node:
            _recurse(item)
    elif isinstance(node, dict):
        for value in node.values():
            _recurse(value)
    else:
        # Handle the base case, where the node is not a list or a dictionary
        pass