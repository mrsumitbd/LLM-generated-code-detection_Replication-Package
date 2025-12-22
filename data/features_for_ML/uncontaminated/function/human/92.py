import typer
from pathlib import Path
from snkmt.core.config import DatabaseConfig
from beaupy import select_multiple, confirm
from typing import Optional
from pathlib import Path

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
    db_path = Path(path).resolve()

    if not db_path.exists():
        typer.echo(f"Warning: Database file does not exist: {db_path}")
        if not confirm("Add anyway?"):
            raise typer.Exit(1)

    if name is None:
        name = db_path.stem

    config = DatabaseConfig()
    try:
        config.add_database(db_path, name)
        typer.echo(f"Added database: {name} -> {db_path}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)