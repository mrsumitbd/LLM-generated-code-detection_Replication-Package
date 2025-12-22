from cached_property import cached_property

class AsyncExchangesResourceWithStreamingResponse:
    def __init__(self, exchanges: AsyncExchangesResource) -> None:
        self._exchanges = exchanges

    @cached_property
    def tickers(self) -> AsyncTickersResourceWithStreamingResponse:
        return AsyncTickersResourceWithStreamingResponse(self._exchanges)

    @cached_property
    def volume_chart(self) -> AsyncVolumeChartResourceWithStreamingResponse:
        return AsyncVolumeChartResourceWithStreamingResponse(self._exchanges)

class AsyncTickersResourceWithStreamingResponse:
    def __init__(self, exchanges: AsyncExchangesResource) -> None:
        self._exchanges = exchanges

class AsyncVolumeChartResourceWithStreamingResponse:
    def __init__(self, exchanges: AsyncExchangesResource) -> None:
        self._exchanges = exchanges