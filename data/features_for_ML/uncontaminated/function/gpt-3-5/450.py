def mount_static_files(app: FastAPI, param: ApplicationConfig):
    static_dir = param.static_dir
    if static_dir:
        app.mount("/static", StaticFiles(directory=static_dir), name="static")