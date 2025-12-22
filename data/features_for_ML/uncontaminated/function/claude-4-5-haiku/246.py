def _split_newline(line: str) -> tuple[str, str]:
    """Split a line at the first newline character.
    
    Returns a tuple of (content_before_newline, newline_and_after).
    If no newline is found, returns (line, '').
    """
    newline_index = line.find('\n')
    if newline_index == -1:
        return (line, '')
    return (line[:newline_index], line[newline_index:])