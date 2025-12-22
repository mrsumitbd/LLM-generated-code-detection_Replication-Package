def mount_static_files(app: FastAPI, param: ApplicationConfig):
    app.mount("/static", StaticFiles(directory=param.STATIC_FILES_DIR), name="static")