from functools import cached_property

class AsyncExchangesResourceWithStreamingResponse:

    def __init__(self, exchanges: AsyncExchangesResource) -> None:
        self.exchanges = exchanges

    @cached_property
    def tickers(self) -> AsyncTickersResourceWithStreamingResponse:
        return AsyncTickersResourceWithStreamingResponse(self.exchanges)

    @cached_property
    def volume_chart(self) -> AsyncVolumeChartResourceWithStreamingResponse:
        return AsyncVolumeChartResourceWithStreamingResponse(self.exchanges)