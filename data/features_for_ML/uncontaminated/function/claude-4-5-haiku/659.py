def print_themed(text: str, style: str = "info") -> None:
    """Print text with themed styling - backward compatibility.

    Args:
        text: Text to print with styling.
        style: Rich style name to apply.
    """
    from rich.console import Console
    
    console = Console()
    console.print(text, style=style)