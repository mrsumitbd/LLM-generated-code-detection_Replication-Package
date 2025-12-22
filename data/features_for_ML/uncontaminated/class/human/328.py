from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncTokenPriceResourceWithStreamingResponse:
    def __init__(self, token_price: AsyncTokenPriceResource) -> None:
        self._token_price = token_price

        self.get_addresses = async_to_streamed_response_wrapper(
            token_price.get_addresses,
        )