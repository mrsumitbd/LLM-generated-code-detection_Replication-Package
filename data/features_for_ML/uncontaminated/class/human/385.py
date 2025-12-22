from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class MarketChartResourceWithStreamingResponse:
    def __init__(self, market_chart: MarketChartResource) -> None:
        self._market_chart = market_chart

        self.get = to_streamed_response_wrapper(
            market_chart.get,
        )
        self.get_range = to_streamed_response_wrapper(
            market_chart.get_range,
        )