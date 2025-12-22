from typing import List, Dict, Any, Optional
from rich.console import Console

def prompt_for_missing_metric_args(
    metric_name: str,
    missing_args: List[str],
    optional_args: List[str],
    default_args: Dict[str, Any],
    console: Optional[Console] = None,
) -> Dict[str, str]:
    user_args = {}
    if console:
        console.print(f"Please provide arguments for metric '{metric_name}':")
    for arg in missing_args:
        user_input = input(f"Enter value for '{arg}': ")
        user_args[arg] = user_input
    for arg in optional_args:
        user_input = input(f"Enter value for '{arg}' (default: {default_args.get(arg)}): ")
        user_args[arg] = user_input if user_input else default_args.get(arg)
    return user_args