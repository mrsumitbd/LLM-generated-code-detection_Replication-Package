from functools import cached_property

class AsyncTokensResourceWithStreamingResponse:

    def __init__(self, tokens: AsyncTokensResource) -> None:
        pass

    @cached_property
    def multi(self) -> AsyncMultiResourceWithStreamingResponse:
        pass

    @cached_property
    def info(self) -> AsyncInfoResourceWithStreamingResponse:
        pass

    @cached_property
    def top_holders(self) -> AsyncTopHoldersResourceWithStreamingResponse:
        pass

    @cached_property
    def holders_chart(self) -> AsyncHoldersChartResourceWithStreamingResponse:
        pass

    @cached_property
    def ohlcv(self) -> AsyncOhlcvResourceWithStreamingResponse:
        pass

    @cached_property
    def pools(self) -> AsyncPoolsResourceWithStreamingResponse:
        pass

    @cached_property
    def trades(self) -> AsyncTradesResourceWithStreamingResponse:
        pass