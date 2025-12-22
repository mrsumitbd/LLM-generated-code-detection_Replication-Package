import os
import yaml
from pathlib import Path
from typing import Optional

import typer

def config_add(
    path: str = typer.Argument(help="Path to the database file to add."),
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Display name for the database (default: filename stem).",
    ),
):
    """Add a database to the configuration file."""
    # Resolve the database path
    db_path = Path(path).expanduser().resolve()

    # Determine the configuration file location
    config_dir = Path(os.getenv("CONFIG_DIR", Path.home() / ".config" / "typerdb"))
    config_file = config_dir / "config.yaml"

    # Ensure the config directory exists
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load existing configuration
    if config_file.exists():
        try:
            with config_file.open("r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
        except Exception as exc:
            typer.echo(f"Error reading config file: {exc}", err=True)
            raise typer.Exit(1)
    else:
        cfg = {}

    # Ensure the databases list exists
    db_list = cfg.get("databases", [])

    # Check for duplicates
    for entry in db_list:
        if Path(entry.get("path", "")).resolve() == db_path:
            typer.echo(f"Database '{db_path}' is already in the configuration.", err=True)
            raise typer.Exit(0)

    # Determine display name
    display_name = name if name is not None else db_path.stem

    # Append new entry
    db_list.append({"path": str(db_path), "name": display_name})
    cfg["databases"] = db_list

    # Write back configuration
    try:
        with config_file.open("w", encoding="utf-8") as f:
            yaml.safe_dump(cfg, f, default_flow_style=False, sort_keys=False)
    except Exception as exc:
        typer.echo(f"Error writing config file: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Added database '{display_name}' ({db_path}) to configuration.")