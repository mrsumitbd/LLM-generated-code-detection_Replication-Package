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
    import json
    from pathlib import Path
    
    config_file = Path.home() / ".config" / "myapp" / "config.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    db_path = Path(path).resolve()
    
    if not db_path.exists():
        typer.echo(f"Error: Database file not found at {db_path}", err=True)
        raise typer.Exit(code=1)
    
    display_name = name if name else db_path.stem
    
    if config_file.exists():
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = {"databases": []}
    
    if "databases" not in config:
        config["databases"] = []
    
    for db in config["databases"]:
        if db["path"] == str(db_path):
            typer.echo(f"Database already exists: {display_name}")
            raise typer.Exit(code=1)
    
    config["databases"].append({
        "name": display_name,
        "path": str(db_path)
    })
    
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    typer.echo(f"Added database '{display_name}' at {db_path}")