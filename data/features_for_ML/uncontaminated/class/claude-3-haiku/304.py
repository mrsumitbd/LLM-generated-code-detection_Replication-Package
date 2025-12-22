class AsyncTokenPriceResourceWithRawResponse:
    def __init__(self, token_price: AsyncTokenPriceResource) -> None:
        self.token_price = token_price

    async def get_price(self, token_address: str) -> Tuple[float, dict]:
        response = await self.token_price.get_price(token_address)
        return response, response.raw_response

    async def get_prices(self, token_addresses: List[str]) -> Tuple[List[float], List[dict]]:
        responses = await self.token_price.get_prices(token_addresses)
        prices = [response.price for response in responses]
        raw_responses = [response.raw_response for response in responses]
        return prices, raw_responses