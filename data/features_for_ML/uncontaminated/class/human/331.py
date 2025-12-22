import anyio
from ._client import Reducto, AsyncReducto

class AsyncAPIResource:
    _client: AsyncReducto

    def __init__(self, client: AsyncReducto) -> None:
        self._client = client
        self._get = client.get
        self._post = client.post
        self._patch = client.patch
        self._put = client.put
        self._delete = client.delete
        self._get_api_list = client.get_api_list

    async def _sleep(self, seconds: float) -> None:
        await anyio.sleep(seconds)