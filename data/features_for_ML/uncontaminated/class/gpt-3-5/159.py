from typing import Any

class CoingeckoWithStreamedResponse:

    def __init__(self, client: Coingecko) -> None:
        self.client = client

    def get_streamed_response(self, endpoint: str) -> Any:
        response = self.client.get(endpoint)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk