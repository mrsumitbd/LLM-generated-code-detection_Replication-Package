from typing import Optional
from fastapi import FastAPI
from fastapi.routing import APIRouter

class Server:

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, app_name: str = "MaiMCore"):
        self.host = host
        self.port = port
        self.app_name = app_name
        self.app = FastAPI(title=app_name)

    def register_router(self, router: APIRouter, prefix: str = ""):
        self.app.include_router(router, prefix=prefix)

    def set_address(self, host: Optional[str] = None, port: Optional[int] = None):
        self.host = host
        self.port = port

    def get_app(self) -> FastAPI:
        return self.app