def get_line1(id: LineFill) -> Line | NA:
    """
    Returns the ID of the first line used in the id linefill.

    :param id: A linefill object
    :return: First line object
    """
    if id.lines:
        return id.lines[0]
    else:
        return NA