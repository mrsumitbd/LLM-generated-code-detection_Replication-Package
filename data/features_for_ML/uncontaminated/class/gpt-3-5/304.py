from typing import Any
from async_token_price_resource import AsyncTokenPriceResource

class AsyncTokenPriceResourceWithRawResponse:

    def __init__(self, token_price: AsyncTokenPriceResource) -> None:
        self.token_price = token_price

    async def get_token_price_with_raw_response(self, token: str) -> Any:
        raw_response = await self.token_price.get_token_price(token)
        return raw_response