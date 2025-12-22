from typing import Optional
from fastapi import FastAPI, APIRouter


class Server:
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, app_name: str = "MaiMCore"):
        self.host = host
        self.port = port
        self.app_name = app_name
        self._app = FastAPI(title=self.app_name)

    def register_router(self, router: APIRouter, prefix: str = ""):
        """Attach an APIRouter to the FastAPI application with an optional prefix."""
        self._app.include_router(router, prefix=prefix)

    def set_address(self, host: Optional[str] = None, port: Optional[int] = None):
        """Set the host and port for the server."""
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port

    def get_app(self) -> FastAPI:
        """Return the underlying FastAPI application."""
        return self._app