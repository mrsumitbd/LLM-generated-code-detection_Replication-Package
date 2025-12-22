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
    user_args = {}

    if console:
        console.print(f"Missing arguments for metric '{metric_name}':")

    for arg in missing_args:
        user_input = input(f"Enter value for '{arg}': ")
        user_args[arg] = user_input

    for arg in optional_args:
        default_value = default_args.get(arg, "")
        user_input = input(f"Enter value for '{arg}' (default: {default_value}): ")
        user_args[arg] = user_input if user_input else default_value

    return user_args