from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.prompt import Prompt

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
    if console is None:
        console = Console()

    console.print(
        f"\n[yellow]Metric '{metric_name}' has configurable arguments[/yellow]"
    )

    args = {}

    # Prompt for required arguments
    if missing_args:
        console.print("[red]Required arguments:[/red]")
        for arg_name in missing_args:
            value = Prompt.ask(f"Enter value for [cyan]{arg_name}[/cyan]")
            args[arg_name] = value

    # Prompt for optional arguments
    if optional_args:
        console.print("[blue]Optional arguments (press Enter to use default):[/blue]")
        for arg_name in optional_args:
            default_value = default_args.get(arg_name, "")
            default_display = f" (default: {default_value})" if default_value else ""
            value = Prompt.ask(
                f"Enter value for [cyan]{arg_name}[/cyan]{default_display}", default=""
            )
            if value:  # Only add if user provided a value
                args[arg_name] = value

    return args