from typing import Any, Literal, cast
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

class App:
        def __init__(self, manager: StreamableHTTPSessionManager) -> None:
            self._manager = manager

        async def __call__(self, scope: Any, receive: Any, send: Any):
            await self._manager.handle_request(scope, receive, send)