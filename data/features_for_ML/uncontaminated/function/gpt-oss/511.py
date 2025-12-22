def flow_initial_velocity_toggle(value):
    """
    Toggle the initial velocity flag or value.

    Parameters
    ----------
    value : bool | int | float
        The current state of the initial velocity. For booleans, the function
        returns the logical negation. For numeric values, it toggles between
        0 and 1 (interpreting any non‑zero value as 1).

    Returns
    -------
    bool | int
        The toggled state.

    Raises
    ------
    TypeError
        If the input type is not supported.
    """
    # Handle boolean input
    if isinstance(value, bool):
        return not value

    # Handle numeric input (int or float)
    if isinstance(value, (int, float)):
        # Treat any non‑zero as 1, zero as 0
        return 0 if value else 1

    # Unsupported type
    raise TypeError(
        f"Unsupported type {type(value).__name__} for flow_initial_velocity_toggle"
    )