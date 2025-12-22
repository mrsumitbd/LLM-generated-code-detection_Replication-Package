class AsyncAPIResource:
    def __init__(self, client: AsyncReducto) -> None:
        self.client = client

    async def _request(self, method: str, path: str, **kwargs):
        url = f"{self.client.base_url.rstrip('/')}/{path.lstrip('/')}"
        return await self.client.request(method, url, **kwargs)

    async def get(self, path: str, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs):
        return await self._request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs):
        return await self._request("DELETE", path, **kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} client={self.client!r}>"