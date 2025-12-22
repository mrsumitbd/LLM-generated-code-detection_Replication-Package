from cached_property import cached_property
from .async_multi_resource_with_streaming_response import AsyncMultiResourceWithStreamingResponse
from .async_info_resource_with_streaming_response import AsyncInfoResourceWithStreamingResponse
from .async_top_holders_resource_with_streaming_response import AsyncTopHoldersResourceWithStreamingResponse
from .async_holders_chart_resource_with_streaming_response import AsyncHoldersChartResourceWithStreamingResponse
from .async_ohlcv_resource_with_streaming_response import AsyncOhlcvResourceWithStreamingResponse
from .async_pools_resource_with_streaming_response import AsyncPoolsResourceWithStreamingResponse
from .async_trades_resource_with_streaming_response import AsyncTradesResourceWithStreamingResponse

class AsyncTokensResourceWithStreamingResponse:
    def __init__(self, tokens: AsyncTokensResource) -> None:
        self.tokens = tokens

    @cached_property
    def multi(self) -> AsyncMultiResourceWithStreamingResponse:
        return AsyncMultiResourceWithStreamingResponse(self.tokens)

    @cached_property
    def info(self) -> AsyncInfoResourceWithStreamingResponse:
        return AsyncInfoResourceWithStreamingResponse(self.tokens)

    @cached_property
    def top_holders(self) -> AsyncTopHoldersResourceWithStreamingResponse:
        return AsyncTopHoldersResourceWithStreamingResponse(self.tokens)

    @cached_property
    def holders_chart(self) -> AsyncHoldersChartResourceWithStreamingResponse:
        return AsyncHoldersChartResourceWithStreamingResponse(self.tokens)

    @cached_property
    def ohlcv(self) -> AsyncOhlcvResourceWithStreamingResponse:
        return AsyncOhlcvResourceWithStreamingResponse(self.tokens)

    @cached_property
    def pools(self) -> AsyncPoolsResourceWithStreamingResponse:
        return AsyncPoolsResourceWithStreamingResponse(self.tokens)

    @cached_property
    def trades(self) -> AsyncTradesResourceWithStreamingResponse:
        return AsyncTradesResourceWithStreamingResponse(self.tokens)