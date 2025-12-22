def escape_discord_formatting(text: str) -> str:
    """
    Escape Discord formatting characters.

    Args:
        text: Text to escape

    Returns:
        Text with escaped formatting
    """
    # Discord formatting characters that need to be escaped
    formatting_chars = ['\\', '*', '_', '~', '`', '|']
    
    result = text
    for char in formatting_chars:
        result = result.replace(char, '\\' + char)
    
    return result