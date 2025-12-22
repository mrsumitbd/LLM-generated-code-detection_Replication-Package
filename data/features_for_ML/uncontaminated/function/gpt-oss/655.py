import xarray as xr
from typing import Dict

def flatten_datatree_as_dict(
    datatree: xr.DataTree, prefix: str = "", sep: str = "/"
) -> Dict[str, xr.Dataset]:
    """
    Flatten a given data tree into a mapping from keys to datasets.

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
    result: Dict[str, xr.Dataset] = {}

    def _visit(node: xr.DataTree, current_path: str) -> None:
        # Add the dataset of the current node if it exists
        if getattr(node, "data", None) is not None:
            key = current_path
            if prefix:
                key = f"{prefix}{sep}{key}" if key else prefix
            result[key] = node.data

        # Recurse into children
        for child_name, child_node in getattr(node, "children", {}).items():
            child_path = f"{current_path}{sep}{child_name}" if current_path else child_name
            _visit(child_node, child_path)

    # Start recursion from the root node
    _visit(datatree, "")

    return result