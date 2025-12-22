from typing import Annotated

import typer
import uvicorn

# Try to import the FastAPI application that should be defined elsewhere in the package.
# If it cannot be imported, create a minimal placeholder application.
try:
    from .app import app  # type: ignore
except Exception:  # pragma: no cover
    from fastapi import FastAPI

    app = FastAPI()


def serve(
    host: Annotated[str, typer.Option(help="Host IP address")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Port number")] = 8000,
    num_workers: Annotated[int, typer.Option(help="Number of worker processes")] = 1,
) -> None:
    """Start running this Tesseract's web server."""
    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=num_workers,
        log_level="info",
    )