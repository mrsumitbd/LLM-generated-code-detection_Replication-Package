import json
import os
from pathlib import Path
import typer

# Define a simple static list of available repositories for demonstration.
# In a real application this could be loaded from a remote source or a config file.
AVAILABLE_REPOS = [
    {"id": 1, "name": "Main Repository", "url": "https://example.com/main"},
    {"id": 2, "name": "Backup Repository", "url": "https://example.com/backup"},
    {"id": 3, "name": "Experimental Repository", "url": "https://example.com/exp"},
]

CONFIG_FILE = Path.home() / ".repo_config.json"


def _load_config() -> dict:
    """Load the repository configuration from the config file."""
    if CONFIG_FILE.is_file():
        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # If the file is corrupted, start fresh.
            return {}
    return {}


def _save_config(config: dict) -> None:
    """Save the repository configuration to the config file."""
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def repo(
    set_default: int | None = typer.Option(
        None, "--set-default", "-s", help="Set default repository ID"
    ),
    clear: bool = typer.Option(False, "--clear", "-c", help="Clear repository configuration"),
    list_config: bool = typer.Option(False, "--list", "-l", help="List current repository configuration"),
    list_repos: bool = typer.Option(False, "--list-repos", "-lr", help="List available repositories"),
):
    """Manage repository configuration and environment variables."""
    # Load existing configuration
    config = _load_config()

    # Handle clear option
    if clear:
        if CONFIG_FILE.is_file():
            CONFIG_FILE.unlink()
            typer.echo("Repository configuration cleared.")
        else:
            typer.echo("No configuration file found to clear.")
        # If clear is requested, ignore other options
        return

    # Handle set_default option
    if set_default is not None:
        # Validate that the ID exists in AVAILABLE_REPOS
        if any(repo["id"] == set_default for repo in AVAILABLE_REPOS):
            config["default_repo"] = set_default
            _save_config(config)
            typer.echo(f"Default repository set to ID {set_default}.")
        else:
            typer.echo(f"Repository ID {set_default} not found in available repositories.")
        # If set_default is requested, ignore other options
        return

    # Handle list_config option
    if list_config:
        if config:
            typer.echo("Current repository configuration:")
            for key, value in config.items():
                typer.echo(f"  {key}: {value}")
        else:
            typer.echo("No repository configuration found.")
        return

    # Handle list_repos option
    if list_repos:
        typer.echo("Available repositories:")
        for repo in AVAILABLE_REPOS:
            typer.echo(f"  ID: {repo['id']}")
            typer.echo(f"    Name: {repo['name']}")
            typer.echo(f"    URL: {repo['url']}")
        return

    # If no options were provided, show help
    typer.echo("No action specified. Use --help for usage information.")