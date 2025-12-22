from rich.console import Console
from rich.style import Style

def print_themed(text: str, style: str = "info") -> None:
    """Print text with themed styling - backward compatibility.

    Args:
        text: Text to print with styling.
        style: Rich style name to apply.
    """
    console = Console()
    if style == "info":
        console.print(text, style="blue")
    elif style == "warning":
        console.print(text, style="yellow")
    elif style == "error":
        console.print(text, style="red")
    else:
        console.print(text, style=Style.parse(style))