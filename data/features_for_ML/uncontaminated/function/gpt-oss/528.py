def chessboard(*args, **kwargs):
    """
    Return a string representation of a chessboard pattern.

    Parameters
    ----------
    *args
        The first positional argument may be the board size (int).
    **kwargs
        - size (int): board size (overrides positional argument if present).
        - char1 (str): character for the first cell of the first row.
        - char2 (str): character for the second cell of the first row.
        - reverse (bool): if True, start the first row with char2 instead of char1.

    Returns
    -------
    str
        The chessboard pattern with rows separated by newline characters.
    """
    # Determine board size
    size = None
    if args:
        try:
            size = int(args[0])
        except Exception:
            size = None
    if 'size' in kwargs:
        try:
            size = int(kwargs['size'])
        except Exception:
            size = None
    if size is None or size <= 0:
        return ""

    # Determine characters
    char1 = kwargs.get('char1', 'X')
    char2 = kwargs.get('char2', 'O')
    reverse = kwargs.get('reverse', False)

    # Build rows
    rows = []
    for i in range(size):
        row = []
        for j in range(size):
            # Determine which character to use
            if (i + j) % 2 == 0:
                ch = char2 if reverse else char1
            else:
                ch = char1 if reverse else char2
            row.append(ch)
        rows.append(''.join(row))
    return '\n'.join(rows)