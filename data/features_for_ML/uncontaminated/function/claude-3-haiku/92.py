import typer
from pathlib import Path
from typing import Optional

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
    config_file = Path("~/.myapp/config.json").expanduser()
    config_file.parent.mkdir(exist_ok=True)

    if not config_file.exists():
        config_file.write_text("{}")

    import json
    config = json.load(config_file.open())

    if name is None:
        name = Path(path).stem

    config[name] = path

    config_file.write_text(json.dumps(config, indent=2))
    typer.echo(f"Added '{name}' to the configuration file.")