def apply_format(text, format_type):
    """
    Applies the specified formatting to the given text.

    Args:
        text (str): The text to be formatted.
        format_type (str): The type of formatting to apply. Can be 'uppercase', 'lowercase', or 'capitalize'.

    Returns:
        str: The formatted text.
    """
    if format_type == 'uppercase':
        return text.upper()
    elif format_type == 'lowercase':
        return text.lower()
    elif format_type == 'capitalize':
        return text.capitalize()
    else:
        return text