import json
from typing import Generator

class CoingeckoWithStreamedResponse:
    def __init__(self, client: Coingecko) -> None:
        self.client = client

    def get_coins_markets(self, vs_currency: str, **kwargs) -> Generator[dict, None, None]:
        response = self.client.get_coins_markets(vs_currency, **kwargs)
        yield from self._stream_response(response)

    def get_coin_by_id(self, id: str, **kwargs) -> Generator[dict, None, None]:
        response = self.client.get_coin_by_id(id, **kwargs)
        yield from self._stream_response(response)

    def _stream_response(self, response: dict) -> Generator[dict, None, None]:
        for item in response.json():
            yield item