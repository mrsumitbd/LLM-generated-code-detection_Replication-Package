def log(msg: str, return_line=False, pre_return_line=False, *args, **kwargs):
    """
    Simple logging helper.

    Parameters
    ----------
    msg : str
        The message format string.
    return_line : bool, optional
        If True, return the formatted string instead of printing it.
    pre_return_line : bool, optional
        If True, print the formatted string and then return it.
    *args, **kwargs
        Arguments for string formatting.

    Returns
    -------
    str or None
        The formatted string if `return_line` or `pre_return_line` is True,
        otherwise None.
    """
    # Format the message safely
    try:
        if args or kwargs:
            formatted = msg.format(*args, **kwargs)
        else:
            formatted = msg
    except Exception:
        # Fallback: use old-style formatting if format fails
        try:
            formatted = msg % args if args else msg
        except Exception:
            formatted = msg

    # Decide what to do based on flags
    if pre_return_line:
        print(formatted)
        return formatted
    if return_line:
        return formatted

    print(formatted)
    return None