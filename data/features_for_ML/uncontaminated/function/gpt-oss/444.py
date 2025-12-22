def check_optimizer_groups(optimizer_groups):
    """
    Validate the structure of optimizer groups.

    Parameters
    ----------
    optimizer_groups : list
        A list of dictionaries, each representing an optimizer group.

    Returns
    -------
    bool
        True if all groups are valid.

    Raises
    ------
    TypeError
        If optimizer_groups is not a list or a group is not a dict.
    KeyError
        If a required key is missing in a group.
    ValueError
        If a group contains invalid types for 'params' or 'lr'.
    """
    if not isinstance(optimizer_groups, list):
        raise TypeError(f"optimizer_groups must be a list, got {type(optimizer_groups).__name__}")

    required_keys = {"params", "lr"}
    for idx, group in enumerate(optimizer_groups):
        if not isinstance(group, dict):
            raise TypeError(f"Group at index {idx} must be a dict, got {type(group).__name__}")

        missing = required_keys - group.keys()
        if missing:
            raise KeyError(f"Group at index {idx} is missing required keys: {missing}")

        params = group["params"]
        lr = group["lr"]

        if not isinstance(params, (list, tuple)):
            raise ValueError(f"'params' in group at index {idx} must be a list or tuple, got {type(params).__name__}")

        if not isinstance(lr, (int, float)):
            raise ValueError(f"'lr' in group at index {idx} must be a number, got {type(lr).__name__}")

    return True