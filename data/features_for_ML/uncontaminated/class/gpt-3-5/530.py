from typing import Any
from async_ping_resource import AsyncPingResource

class AsyncPingResourceWithRawResponse:

    def __init__(self, ping: AsyncPingResource) -> None:
        self.ping = ping

    async def get_response(self) -> Any:
        return await self.ping.get_response()