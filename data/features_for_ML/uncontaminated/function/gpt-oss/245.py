def _get_colored_text(text: str, color: str) -> str:
    """
    Get the colored version of the input text.

    Args:
        text (str): Input text.
        color (str): Color to be applied to the text.

    Returns:
        str: Colored version of the input text.
    """
    # ANSI color codes for standard colors
    ansi_codes = {
        "black":   "30",
        "red":     "31",
        "green":   "32",
        "yellow":  "33",
        "blue":    "34",
        "magenta": "35",
        "cyan":    "36",
        "white":   "37",
        # Bright variants
        "bright_black":   "90",
        "bright_red":     "91",
        "bright_green":   "92",
        "bright_yellow":  "93",
        "bright_blue":    "94",
        "bright_magenta": "95",
        "bright_cyan":    "96",
        "bright_white":   "97",
    }

    # Normalize the color string
    key = color.strip().lower().replace(" ", "_")
    code = ansi_codes.get(key)

    if code is None:
        # If the color is not recognized, return the original text
        return text

    # Wrap the text with ANSI escape codes
    return f"\033[{code}m{text}\033[0m"