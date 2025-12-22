def remove_illegal_characters(text):
    """
    Remove ASCII control characters from the input string, except for
    tab (`\t`), newline (`\n`), and carriage return (`\r`).

    Parameters
    ----------
    text : str
        The input string from which to remove illegal characters.

    Returns
    -------
    str
        The cleaned string with illegal characters removed.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    # Keep tab, newline, carriage return, printable ASCII (32-126),
    # and all non-ASCII characters (ord > 127).
    allowed = ('\t', '\n', '\r')
    result = []
    for ch in text:
        o = ord(ch)
        if ch in allowed or (32 <= o <= 126) or o > 127:
            result.append(ch)
    return ''.join(result)