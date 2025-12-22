def _is_true(valid) -> bool:
    """
    Determine if the given value should be considered True.

    The function treats the following string values (case‑insensitive) as True:
        'true', '1', 'yes', 'y', 't'

    All other string values are considered False. For non‑string values,
    Python's built‑in truthiness rules are used.

    Parameters
    ----------
    valid : Any
        The value to evaluate.

    Returns
    -------
    bool
        True if the value is considered truthy, False otherwise.
    """
    if isinstance(valid, str):
        return valid.strip().lower() in {"true", "1", "yes", "y", "t"}
    return bool(valid)