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
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m',
    }
    
    color_code = color_codes.get(color.lower(), '')
    reset_code = color_codes['reset']
    
    return f"{color_code}{text}{reset_code}"