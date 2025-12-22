def escape_discord_formatting(text: str) -> str:
    """
    Escape Discord formatting characters.

    Args:
        text: Text to escape

    Returns:
        Text with escaped formatting
    """
    # Discord formatting characters that need escaping
    # According to Discord docs: *, _, ~, `, >, |, (, ), [, ], {, }, !
    # We escape each by prefixing with a backslash.
    escape_chars = {'*', '_', '~', '`', '>', '|', '(', ')', '[', ']', '{', '}', '!'}
    # Build result
    result = []
    for ch in text:
        if ch in escape_chars:
            result.append('\\' + ch)
        else:
            result.append(ch)
    return ''.join(result)