import asyncio
from typing import AsyncGenerator

class AsyncTokenPriceResource:
    async def get_token_price(self, token_id: str) -> float:
        # Implementation of the AsyncTokenPriceResource class
        pass

class AsyncTokenPriceResourceWithStreamingResponse:
    def __init__(self, token_price: AsyncTokenPriceResource) -> None:
        self.token_price = token_price

    async def get_token_price_stream(self, token_id: str) -> AsyncGenerator[float, None]:
        while True:
            price = await self.token_price.get_token_price(token_id)
            yield price
            await asyncio.sleep(1)