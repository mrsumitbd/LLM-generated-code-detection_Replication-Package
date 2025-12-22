def mount_static_files(app: FastAPI, param: ApplicationConfig):
    """Mount static files to the FastAPI application."""
    import os
    from fastapi.staticfiles import StaticFiles
    
    # Get the static directory path from config or use default
    static_dir = getattr(param, 'static_dir', 'static')
    
    # Check if static directory exists
    if os.path.isdir(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")