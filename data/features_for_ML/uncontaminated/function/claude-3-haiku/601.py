def escape_discord_formatting(text: str) -> str:
    """
    Escape Discord formatting characters.

    Args:
        text: Text to escape

    Returns:
        Text with escaped formatting
    """
    return text.replace("\\", "\\\\").replace("_", "\\_").replace("*", "\\*").replace("~", "\\~").replace("`", "\\`").replace("|", "\\|")