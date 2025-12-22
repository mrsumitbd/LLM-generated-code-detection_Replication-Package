from fastapi.staticfiles import StaticFiles
from pathlib import Path

def mount_static_files(app: FastAPI, param: ApplicationConfig):
    """
    Mount static files for a FastAPI application.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.
    param : ApplicationConfig
        Configuration object that should provide at least the following
        attributes:
            - static_dir (str or Path): Directory containing static files.
            - static_url_path (str): URL path where static files will be served.
            - static_html (bool, optional): Whether to serve index.html on
              directory requests. Defaults to False.
    """
    # Ensure required attributes exist
    if not hasattr(param, "static_dir") or not hasattr(param, "static_url_path"):
        return

    static_dir = Path(param.static_dir)
    if not static_dir.is_dir():
        # If the directory does not exist, do not mount anything.
        return

    # Optional flag to serve index.html on directory requests
    static_html = getattr(param, "static_html", False)

    app.mount(
        param.static_url_path,
        StaticFiles(directory=str(static_dir), html=static_html),
        name="static",
    )