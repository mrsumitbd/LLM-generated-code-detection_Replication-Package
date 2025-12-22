import asyncio
from typing import Tuple

class AsyncPingResourceWithRawResponse:
    def __init__(self, ping: AsyncPingResource) -> None:
        self._ping = ping

    async def ping(self, host: str, timeout: float = 1.0) -> Tuple[bool, bytes]:
        try:
            start_time = asyncio.get_event_loop().time()
            response = await self._ping.ping(host, timeout)
            end_time = asyncio.get_event_loop().time()
            return True, response
        except asyncio.TimeoutError:
            return False, b''
        except Exception:
            return False, b''
        finally:
            pass