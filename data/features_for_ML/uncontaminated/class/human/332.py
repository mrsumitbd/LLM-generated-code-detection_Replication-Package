import time
from ._client import Reducto, AsyncReducto

class SyncAPIResource:
    _client: Reducto

    def __init__(self, client: Reducto) -> None:
        self._client = client
        self._get = client.get
        self._post = client.post
        self._patch = client.patch
        self._put = client.put
        self._delete = client.delete
        self._get_api_list = client.get_api_list

    def _sleep(self, seconds: float) -> None:
        time.sleep(seconds)