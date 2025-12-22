def get_line1(id: LineFill) -> Line | NA:
    """
    Returns the ID of the first line used in the id linefill.

    :param id: A linefill object
    :return: First line object
    """
    # If the object is None or has no lines attribute, return NA
    if id is None:
        return NA

    # Try to access a list/tuple of lines
    lines = None
    if hasattr(id, "lines"):
        lines = getattr(id, "lines")
    elif hasattr(id, "line_list"):
        lines = getattr(id, "line_list")
    elif hasattr(id, "line"):
        # Some implementations might store a single line in `line`
        lines = [getattr(id, "line")]

    # If we found a sequence, return the first element
    if isinstance(lines, (list, tuple, set)):
        try:
            return next(iter(lines))
        except StopIteration:
            return NA

    # If we found a single line object, return it
    if isinstance(lines, Line):
        return lines

    # Fallback: try to get the first attribute that looks like a Line
    for attr in dir(id):
        if attr.startswith("_"):
            continue
        val = getattr(id, attr)
        if isinstance(val, Line):
            return val

    # If nothing found, return NA
    return NA