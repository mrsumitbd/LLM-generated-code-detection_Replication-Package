from typing import Any, Callable, List, Tuple, Union

def get_differentiable_paths(
    apply_endpoint_fn: Callable[[Any], bool],
    inputs: dict[str, Any],
    outputs: dict[str, Any],
) -> Tuple[List[str], List[str]]:
    """
    Get the paths of all differentiable leaves present in the given inputs and outputs.

    Parameters
    ----------
    apply_endpoint_fn : Callable[[Any], bool]
        A function that takes a leaf value and returns ``True`` if the leaf is
        considered differentiable, ``False`` otherwise.
    inputs : dict[str, Any]
        The input dictionary to inspect.
    outputs : dict[str, Any]
        The output dictionary to inspect.

    Returns
    -------
    Tuple[List[str], List[str]]
        Two lists containing the string paths of differentiable leaves in
        ``inputs`` and ``outputs`` respectively.
    """
    def _traverse(
        obj: Any,
        prefix: str,
        result: List[str],
    ) -> None:
        """
        Recursively traverse ``obj`` and collect paths of differentiable leaves.
        """
        # Handle dictionaries
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                _traverse(value, new_prefix, result)
            return

        # Handle lists and tuples
        if isinstance(obj, (list, tuple)):
            for idx, value in enumerate(obj):
                new_prefix = f"{prefix}[{idx}]" if prefix else f"[{idx}]"
                _traverse(value, new_prefix, result)
            return

        # Handle other objects: treat as leaf
        if apply_endpoint_fn(obj):
            result.append(prefix)

    input_paths: List[str] = []
    output_paths: List[str] = []

    _traverse(inputs, "", input_paths)
    _traverse(outputs, "", output_paths)

    return input_paths, output_paths