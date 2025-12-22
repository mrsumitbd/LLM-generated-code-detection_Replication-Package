from typing import List, Dict, Any, Optional
from rich.console import Console

def prompt_for_missing_metric_args(
    metric_name: str,
    missing_args: List[str],
    optional_args: List[str],
    default_args: Dict[str, Any],
    console: Optional[Console] = None,
) -> Dict[str, str]:
    """
    Interactively prompt user for missing metric arguments.

    Args:
        metric_name: Name of the metric
        missing_args: List of missing required argument names
        optional_args: List of optional argument names
        default_args: Dictionary of default values
        console: Console for output

    Returns:
        Dictionary of user-provided arguments
    """
    # Helper to get input, using console if available
    def _get_input(prompt: str) -> str:
        if console is not None:
            return console.input(prompt)
        else:
            return input(prompt)

    # Helper to print messages
    def _print(msg: str) -> None:
        if console is not None:
            console.print(msg)
        else:
            print(msg)

    result: Dict[str, str] = {}

    # Prompt for required missing arguments
    for arg in missing_args:
        while True:
            _print(f"[bold]{metric_name}[/bold] requires argument '{arg}'.")
            value = _get_input(f"Enter value for '{arg}': ").strip()
            if value:
                result[arg] = value
                break
            else:
                _print(f"[red]'{arg}' cannot be empty. Please provide a value.[/red]")

    # Prompt for optional arguments
    for arg in optional_args:
        default = default_args.get(arg)
        if default is not None:
            prompt = f"Enter value for optional argument '{arg}' (default: {default}) [press Enter to skip]: "
        else:
            prompt = f"Enter value for optional argument '{arg}' [press Enter to skip]: "
        value = _get_input(prompt).strip()
        if value:
            result[arg] = value
        elif default is not None:
            result[arg] = str(default)

    return result