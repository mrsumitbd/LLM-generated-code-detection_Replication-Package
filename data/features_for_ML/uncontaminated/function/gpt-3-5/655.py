def flatten_datatree_as_dict(
    datatree: xr.DataTree, prefix: str = "", sep: str = "/"
) -> dict[str, xr.Dataset]:
    result = {}

    def flatten(tree, current_key):
        for key, value in tree.items():
            new_key = f"{current_key}{sep}{key}" if current_key else key
            if isinstance(value, xr.Dataset):
                result[new_key] = value
            elif isinstance(value, xr.DataTree):
                flatten(value, new_key)

    flatten(datatree, prefix)
    return result