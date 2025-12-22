import xarray as xr

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
    datasets = {}
    if datatree.has_data:
        datasets[prefix] = datatree.to_dataset()
    for name, child in datatree.children.items():
        child_prefix = f"{prefix}{sep}{name}" if prefix else name
        datasets.update(flatten_datatree_as_dict(child, prefix=child_prefix, sep=sep))
    return datasets