def get_str_len(text, fontSizeSet):
    """
    Compute the maximum pixel width of a string across a set of font sizes.

    Parameters
    ----------
    text : str
        The string to measure.
    fontSizeSet : dict or set
        If a dict, it should map a font size to a mapping of characters to
        their pixel widths.  If a set (or list) of integers, the width of a
        character is assumed to be equal to the font size.

    Returns
    -------
    int
        The maximum width (in pixels) of the string across the provided
        font sizes.  If the input set is empty, 0 is returned.
    """
    # Empty input
    if not text:
        return 0

    # If fontSizeSet is a mapping of font size -> char width mapping
    if isinstance(fontSizeSet, dict):
        max_len = 0
        for size, char_widths in fontSizeSet.items():
            total = 0
            for ch in text:
                total += char_widths.get(ch, 0)
            if total > max_len:
                max_len = total
        return max_len

    # If fontSizeSet is an iterable of font sizes (e.g., set or list)
    try:
        sizes = list(fontSizeSet)
    except TypeError:
        # Not iterable, treat as single size
        sizes = [fontSizeSet]

    if not sizes:
        return 0

    # Assume each character width equals the font size
    max_size = max(sizes)
    return len(text) * max_size