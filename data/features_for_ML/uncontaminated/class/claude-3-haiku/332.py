class SyncAPIResource:
    def __init__(self, client: Reducto) -> None:
        self.client = client

    def _sleep(self, seconds: float) -> None:
        import time
        time.sleep(seconds)

    def create(self, data: dict) -> dict:
        response = self.client.post(self.endpoint, data=data)
        return response.json()

    def retrieve(self, resource_id: str) -> dict:
        response = self.client.get(f"{self.endpoint}/{resource_id}")
        return response.json()

    def update(self, resource_id: str, data: dict) -> dict:
        response = self.client.put(f"{self.endpoint}/{resource_id}", data=data)
        return response.json()

    def delete(self, resource_id: str) -> None:
        self.client.delete(f"{self.endpoint}/{resource_id}")

    def list(self, **params) -> list:
        response = self.client.get(self.endpoint, params=params)
        return response.json()