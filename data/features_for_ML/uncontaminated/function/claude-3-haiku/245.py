def _get_colored_text(text: str, color: str) -> str:
    """
    Get the colored version of the input text.

    Args:
        text (str): Input text.
        color (str): Color to be applied to the text.

    Returns:
        str: Colored version of the input text.
    """
    color_codes = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }

    if color.lower() in color_codes:
        return f"{color_codes[color.lower()]}{text}\033[0m"
    else:
        return text