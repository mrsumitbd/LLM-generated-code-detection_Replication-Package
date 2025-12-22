def serve(
    host: Annotated[str, typer.Option(help="Host IP address")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Port number")] = 8000,
    num_workers: Annotated[int, typer.Option(help="Number of worker processes")] = 1,
) -> None:
    """Start running this Tesseract's web server."""
    pass