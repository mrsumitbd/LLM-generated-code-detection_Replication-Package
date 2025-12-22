from typing import List, Any

def validate_helper(variable_node: Any, data_type: Any, path: List[str]) -> None:
    """
    Recursively validate that the value stored in `variable_node` matches the
    expected `data_type`.  `path` is a list of identifiers that describes the
    location of the current node in the overall data structure and is used
    for error reporting.

    The function raises a ValueError if a mismatch is found.
    """
    # Helper to format the current location
    def _location() -> str:
        return ".".join(path) if path else "<root>"

    # Resolve the actual value stored in the node
    # We assume the node exposes a `value` attribute; if not, use the node itself.
    value = getattr(variable_node, "value", variable_node)

    # If data_type is a plain Python type, use isinstance
    if isinstance(data_type, type):
        if not isinstance(value, data_type):
            raise ValueError(
                f"Type mismatch at {_location()}: expected {data_type.__name__}, "
                f"got {type(value).__name__}"
            )
        return

    # If data_type has a `kind` attribute, interpret it
    kind = getattr(data_type, "kind", None)

    # Primitive kinds
    if kind in {"int", "float", "str", "bool", "none", "any"}:
        if kind == "any":
            return
        if kind == "none":
            if value is not None:
                raise ValueError(
                    f"Type mismatch at {_location()}: expected None, got {type(value).__name__}"
                )
            return
        expected_type = {"int": int, "float": float, "str": str, "bool": bool}[kind]
        if not isinstance(value, expected_type):
            raise ValueError(
                f"Type mismatch at {_location()}: expected {kind}, got {type(value).__name__}"
            )
        return

    # Composite kinds
    if kind == "list":
        if not isinstance(value, list):
            raise ValueError(
                f"Type mismatch at {_location()}: expected list, got {type(value).__name__}"
            )
        elem_type = getattr(data_type, "element_type", None)
        if elem_type is None:
            return  # No element type specified; accept any
        for idx, elem in enumerate(value):
            validate_helper(elem, elem_type, path + [f"[{idx}]"])
        return

    if kind == "tuple":
        if not isinstance(value, tuple):
            raise ValueError(
                f"Type mismatch at {_location()}: expected tuple, got {type(value).__name__}"
            )
        elem_types = getattr(data_type, "element_types", None)
        if elem_types is None:
            return
        if len(elem_types) != len(value):
            raise ValueError(
                f"Type mismatch at {_location()}: expected tuple of length {len(elem_types)}, "
                f"got length {len(value)}"
            )
        for idx, (elem, elem_type) in enumerate(zip(value, elem_types)):
            validate_helper(elem, elem_type, path + [f"[{idx}]"])
        return

    if kind == "dict":
        if not isinstance(value, dict):
            raise ValueError(
                f"Type mismatch at {_location()}: expected dict, got {type(value).__name__}"
            )
        key_type = getattr(data_type, "key_type", None)
        val_type = getattr(data_type, "value_type", None)
        for k, v in value.items():
            if key_type is not None:
                validate_helper(k, key_type, path + ["<key>"])
            if val_type is not None:
                validate_helper(v, val_type, path + [f"[{k}]"])
        return

    if kind == "set":
        if not isinstance(value, set):
            raise ValueError(
                f"Type mismatch at {_location()}: expected set, got {type(value).__name__}"
            )
        elem_type = getattr(data_type, "element_type", None)
        if elem_type is None:
            return
        for idx, elem in enumerate(value):
            validate_helper(elem, elem_type, path + [f"[{idx}]"])
        return

    # If we reach here, we don't know how to validate this type
    raise ValueError(
        f"Unsupported data type at {_location()}: {data_type!r}"
    )