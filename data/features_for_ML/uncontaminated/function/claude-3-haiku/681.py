def get_differentiable_paths(
    apply_endpoint_fn: Callable, inputs: dict[str, Any], outputs: dict[str, Any]
) -> tuple[list[str], list[str]]:
    """Get the paths of all differentiable leaves present in the given inputs and outputs."""
    input_paths = []
    output_paths = []

    def traverse_dict(path, d):
        for key, value in d.items():
            new_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                traverse_dict(new_path, value)
            else:
                if apply_endpoint_fn(value):
                    if path in inputs:
                        input_paths.append(new_path)
                    if path in outputs:
                        output_paths.append(new_path)

    traverse_dict("", inputs)
    traverse_dict("", outputs)
    return input_paths, output_paths