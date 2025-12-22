def repo(
    set_default: int | None = typer.Option(None, "--set-default", "-s", help="Set default repository ID"),
    clear: bool = typer.Option(False, "--clear", "-c", help="Clear repository configuration"),
    list_config: bool = typer.Option(False, "--list", "-l", help="List current repository configuration"),
    list_repos: bool = typer.Option(False, "--list-repos", "-lr", help="List available repositories"),
):
    """Manage repository configuration and environment variables."""
    import os
    import json
    from pathlib import Path
    
    config_dir = Path.home() / ".config" / "repo_manager"
    config_file = config_dir / "config.json"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config():
        if config_file.exists():
            with open(config_file, "r") as f:
                return json.load(f)
        return {"default_repo": None, "repositories": {}}
    
    def save_config(config):
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    
    config = load_config()
    
    if clear:
        config = {"default_repo": None, "repositories": {}}
        save_config(config)
        typer.echo("Repository configuration cleared.")
        return
    
    if list_config:
        typer.echo("Current Repository Configuration:")
        typer.echo(f"Default Repository ID: {config.get('default_repo', 'Not set')}")
        if config.get("repositories"):
            typer.echo("Repositories:")
            for repo_id, repo_info in config["repositories"].items():
                typer.echo(f"  {repo_id}: {repo_info}")
        else:
            typer.echo("No repositories configured.")
        return
    
    if list_repos:
        typer.echo("Available Repositories:")
        if config.get("repositories"):
            for repo_id, repo_info in config["repositories"].items():
                default_marker = " (default)" if repo_id == config.get("default_repo") else ""
                typer.echo(f"  {repo_id}: {repo_info}{default_marker}")
        else:
            typer.echo("No repositories available.")
        return
    
    if set_default is not None:
        config["default_repo"] = set_default
        save_config(config)
        typer.echo(f"Default repository set to ID: {set_default}")
        return
    
    if not any([set_default is not None, clear, list_config, list_repos]):
        typer.echo("Use --help to see available options.")