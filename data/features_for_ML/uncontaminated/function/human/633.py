import typer

def repo(
    set_default: int | None = typer.Option(None, "--set-default", "-s", help="Set default repository ID"),
    clear: bool = typer.Option(False, "--clear", "-c", help="Clear repository configuration"),
    list_config: bool = typer.Option(False, "--list", "-l", help="List current repository configuration"),
    list_repos: bool = typer.Option(False, "--list-repos", "-lr", help="List available repositories"),
):
    """Manage repository configuration and environment variables."""
    
    # Handle list repositories mode
    if list_repos:
        _list_repositories()
        return
    
    # Handle list config mode
    if list_config:
        _list_repo_config()
        return

    # Handle clear mode
    if clear:
        _clear_repo_config()
        return

    # Handle set default mode
    if set_default is not None:
        _set_default_repository(set_default)
        return

    # No flags provided, launch TUI
    _run_repo_selector_tui()