def print_themed(text: str, style: str = "info") -> None:
    """
    Print text with themed styling - backward compatibility.

    Args:
        text: Text to print with styling.
        style: Rich style name to apply.
    """
    try:
        from rich import print as rprint
        # Use Rich's print with style
        rprint(text, style=style)
    except Exception:
        # Fallback to plain print if Rich is unavailable or any error occurs
        print(text)