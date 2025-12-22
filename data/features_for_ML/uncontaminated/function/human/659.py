from rich.console import Console

def print_themed(text: str, style: str = "info") -> None:
    """Print text with themed styling - backward compatibility.

    Args:
        text: Text to print with styling.
        style: Rich style name to apply.
    """
    console: Console = _theme_manager.get_console()
    console.print(f"[{style}]{text}[/]")