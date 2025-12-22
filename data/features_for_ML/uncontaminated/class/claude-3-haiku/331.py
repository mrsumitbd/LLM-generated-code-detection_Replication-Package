class AsyncAPIResource:
    def __init__(self, client: AsyncReducto) -> None:
        self._client = client

    async def create(self, data: dict) -> dict:
        response = await self._client.post(self._get_endpoint(), data=data)
        return response.json()

    async def retrieve(self, resource_id: str) -> dict:
        response = await self._client.get(f"{self._get_endpoint()}/{resource_id}")
        return response.json()

    async def update(self, resource_id: str, data: dict) -> dict:
        response = await self._client.put(f"{self._get_endpoint()}/{resource_id}", data=data)
        return response.json()

    async def delete(self, resource_id: str) -> None:
        await self._client.delete(f"{self._get_endpoint()}/{resource_id}")

    def _get_endpoint(self) -> str:
        raise NotImplementedError("Subclasses must implement the _get_endpoint method")