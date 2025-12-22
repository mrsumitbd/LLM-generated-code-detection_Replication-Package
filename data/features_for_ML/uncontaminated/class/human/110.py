from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncOhlcvResourceWithRawResponse:
    def __init__(self, ohlcv: AsyncOhlcvResource) -> None:
        self._ohlcv = ohlcv

        self.get_timeframe = async_to_raw_response_wrapper(
            ohlcv.get_timeframe,
        )