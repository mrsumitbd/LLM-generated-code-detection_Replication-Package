def flatten_datatree_as_dict(
    datatree: xr.DataTree, prefix: str = "", sep: str = "/"
) -> dict[str, xr.Dataset]:
    result = {}
    for name, item in datatree.items():
        if isinstance(item, xr.DataTree):
            new_prefix = f"{prefix}{name}{sep}" if prefix else name
            result.update(flatten_datatree_as_dict(item, new_prefix, sep))
        else:
            key = f"{prefix}{name}" if prefix else name
            result[key] = item
    return result