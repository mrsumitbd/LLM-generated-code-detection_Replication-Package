class AsyncExchangesResourceWithStreamingResponse:

    def __init__(self, exchanges: AsyncExchangesResource) -> None:
        self._exchanges = exchanges

    @cached_property
    def tickers(self) -> AsyncTickersResourceWithStreamingResponse:
        return AsyncTickersResourceWithStreamingResponse(self._exchanges.tickers)

    @cached_property
    def volume_chart(self) -> AsyncVolumeChartResourceWithStreamingResponse:
        return AsyncVolumeChartResourceWithStreamingResponse(self._exchanges.volume_chart)