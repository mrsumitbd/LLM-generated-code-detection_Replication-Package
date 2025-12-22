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
    from rich.console import Console as RichConsole
    
    if console is None:
        console = RichConsole()
    
    user_args = {}
    
    # Prompt for missing required arguments
    if missing_args:
        console.print(f"\n[bold]Missing required arguments for {metric_name}:[/bold]")
        for arg in missing_args:
            default_value = default_args.get(arg)
            if default_value is not None:
                prompt_text = f"  {arg} (default: {default_value}): "
            else:
                prompt_text = f"  {arg}: "
            
            value = console.input(prompt_text).strip()
            
            if not value and default_value is not None:
                user_args[arg] = str(default_value)
            elif value:
                user_args[arg] = value
            else:
                user_args[arg] = value
    
    # Prompt for optional arguments
    if optional_args:
        console.print(f"\n[bold]Optional arguments for {metric_name}:[/bold]")
        for arg in optional_args:
            default_value = default_args.get(arg)
            if default_value is not None:
                prompt_text = f"  {arg} (default: {default_value}, press Enter to skip): "
            else:
                prompt_text = f"  {arg} (press Enter to skip): "
            
            value = console.input(prompt_text).strip()
            
            if value:
                user_args[arg] = value
            elif default_value is not None:
                user_args[arg] = str(default_value)
    
    return user_args