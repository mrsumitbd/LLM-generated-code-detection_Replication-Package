class AsyncTokensResourceWithStreamingResponse:

    def __init__(self, tokens: AsyncTokensResource) -> None:
        self._tokens = tokens

    @cached_property
    def multi(self) -> AsyncMultiResourceWithStreamingResponse:
        return AsyncMultiResourceWithStreamingResponse(self._tokens.multi)

    @cached_property
    def info(self) -> AsyncInfoResourceWithStreamingResponse:
        return AsyncInfoResourceWithStreamingResponse(self._tokens.info)

    @cached_property
    def top_holders(self) -> AsyncTopHoldersResourceWithStreamingResponse:
        return AsyncTopHoldersResourceWithStreamingResponse(self._tokens.top_holders)

    @cached_property
    def holders_chart(self) -> AsyncHoldersChartResourceWithStreamingResponse:
        return AsyncHoldersChartResourceWithStreamingResponse(self._tokens.holders_chart)

    @cached_property
    def ohlcv(self) -> AsyncOhlcvResourceWithStreamingResponse:
        return AsyncOhlcvResourceWithStreamingResponse(self._tokens.ohlcv)

    @cached_property
    def pools(self) -> AsyncPoolsResourceWithStreamingResponse:
        return AsyncPoolsResourceWithStreamingResponse(self._tokens.pools)

    @cached_property
    def trades(self) -> AsyncTradesResourceWithStreamingResponse:
        return AsyncTradesResourceWithStreamingResponse(self._tokens.trades)