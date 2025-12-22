def get_differentiable_paths(
    apply_endpoint_fn: Callable, inputs: dict[str, Any], outputs: dict[str, Any]
) -> tuple[list[str], list[str]]:
    
    def _get_leaves(data, path=''):
        leaves = []
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                leaves.extend(_get_leaves(value, new_path))
            else:
                leaves.append(new_path)
        return leaves
    
    input_leaves = _get_leaves(inputs)
    output_leaves = _get_leaves(outputs)
    
    differentiable_paths = []
    for path in input_leaves:
        if apply_endpoint_fn(path):
            differentiable_paths.append(path)
    
    for path in output_leaves:
        if apply_endpoint_fn(path):
            differentiable_paths.append(path)
    
    return input_leaves, output_leaves