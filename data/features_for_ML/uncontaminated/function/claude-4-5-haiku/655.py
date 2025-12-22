def flatten_datatree_as_dict(
    datatree: xr.DataTree, prefix: str = "", sep: str = "/"
) -> dict[str, xr.Dataset]:
    """Flatten a given data tree into a mapping from keys to datasets.

    Useful for quickly investigating the datasets of a deeply nested
    data tree.

    Args:
        datatree: The data tree.
        prefix: Prefix for all keys, defaults to `""`.
        sep: Group name separator string used in keys, defaults to `"/"`.

    Returns:
        A mapping from keys to datasets. Keys are generated
          by concatenating names of nested groups using
          the separator `sep`.
    """
    result = {}
    
    # Add current node's dataset if it exists
    current_key = prefix if prefix else "/"
    if datatree.ds is not None:
        result[current_key] = datatree.ds
    
    # Recursively process children
    for child_name, child_node in datatree.children.items():
        if prefix:
            child_prefix = prefix + sep + child_name
        else:
            child_prefix = sep + child_name
        
        child_dict = flatten_datatree_as_dict(child_node, child_prefix, sep)
        result.update(child_dict)
    
    return result