def _split_newline(line: str) -> tuple[str, str]:
    """Split a string at the first newline character.

    Returns a tuple (before, after). If no newline is present,
    the second element is an empty string.
    """
    idx = line.find('\n')
    if idx == -1:
        return line, ''
    return line[:idx], line[idx + 1:]