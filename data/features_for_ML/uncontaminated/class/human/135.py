from .info import (
    InfoResource,
    AsyncInfoResource,
    InfoResourceWithRawResponse,
    AsyncInfoResourceWithRawResponse,
    InfoResourceWithStreamingResponse,
    AsyncInfoResourceWithStreamingResponse,
)
from .multi import (
    MultiResource,
    AsyncMultiResource,
    MultiResourceWithRawResponse,
    AsyncMultiResourceWithRawResponse,
    MultiResourceWithStreamingResponse,
    AsyncMultiResourceWithStreamingResponse,
)
from .ohlcv import (
    OhlcvResource,
    AsyncOhlcvResource,
    OhlcvResourceWithRawResponse,
    AsyncOhlcvResourceWithRawResponse,
    OhlcvResourceWithStreamingResponse,
    AsyncOhlcvResourceWithStreamingResponse,
)
from .pools import (
    PoolsResource,
    AsyncPoolsResource,
    PoolsResourceWithRawResponse,
    AsyncPoolsResourceWithRawResponse,
    PoolsResourceWithStreamingResponse,
    AsyncPoolsResourceWithStreamingResponse,
)
from .trades import (
    TradesResource,
    AsyncTradesResource,
    TradesResourceWithRawResponse,
    AsyncTradesResourceWithRawResponse,
    TradesResourceWithStreamingResponse,
    AsyncTradesResourceWithStreamingResponse,
)
from ....._compat import cached_property
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .holders_chart import (
    HoldersChartResource,
    AsyncHoldersChartResource,
    HoldersChartResourceWithRawResponse,
    AsyncHoldersChartResourceWithRawResponse,
    HoldersChartResourceWithStreamingResponse,
    AsyncHoldersChartResourceWithStreamingResponse,
)
from .top_holders import (
    TopHoldersResource,
    AsyncTopHoldersResource,
    TopHoldersResourceWithRawResponse,
    AsyncTopHoldersResourceWithRawResponse,
    TopHoldersResourceWithStreamingResponse,
    AsyncTopHoldersResourceWithStreamingResponse,
)

class AsyncTokensResourceWithStreamingResponse:
    def __init__(self, tokens: AsyncTokensResource) -> None:
        self._tokens = tokens

        self.get_address = async_to_streamed_response_wrapper(
            tokens.get_address,
        )

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