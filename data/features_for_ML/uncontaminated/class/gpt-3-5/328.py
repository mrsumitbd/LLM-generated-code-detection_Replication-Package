from typing import List
from asyncio import sleep

class AsyncTokenPriceResourceWithStreamingResponse:

    def __init__(self, token_price: AsyncTokenPriceResource) -> None:
        self.token_price = token_price

    async def get_token_prices_stream(self, interval: int) -> List[float]:
        token_prices = []
        while True:
            price = await self.token_price.get_token_price()
            token_prices.append(price)
            await sleep(interval)
        return token_prices