from fastapi.staticfiles import StaticFiles
from derisk_app.config import ApplicationConfig, ServiceWebParameters, SystemParameters
import os
from derisk.configs.model_config import (
    LOGDIR,
    STATIC_MESSAGE_IMG_PATH,
)
from fastapi import FastAPI

def mount_static_files(app: FastAPI, param: ApplicationConfig):
    if param.service.web.new_web_ui:
        static_file_path = os.path.join(ROOT_PATH, "src", "derisk_app/static/web")
    else:
        static_file_path = os.path.join(ROOT_PATH, "src", "derisk_app/static/old_web")

    os.makedirs(STATIC_MESSAGE_IMG_PATH, exist_ok=True)
    app.mount(
        "/images",
        StaticFiles(directory=STATIC_MESSAGE_IMG_PATH, html=True),
        name="static2",
    )
    # app.mount(
    #     "/_next/static", StaticFiles(directory=static_file_path + "/_next/static")
    # )
    app.mount("/", StaticFiles(directory=static_file_path, html=True), name="static")

    app.mount(
        "/swagger_static",
        StaticFiles(directory=static_file_path),
        name="swagger_static",
    )