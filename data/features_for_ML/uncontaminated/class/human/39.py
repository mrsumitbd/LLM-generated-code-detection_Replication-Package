from .tickers import (
    TickersResource,
    AsyncTickersResource,
    TickersResourceWithRawResponse,
    AsyncTickersResourceWithRawResponse,
    TickersResourceWithStreamingResponse,
    AsyncTickersResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .volume_chart import (
    VolumeChartResource,
    AsyncVolumeChartResource,
    VolumeChartResourceWithRawResponse,
    AsyncVolumeChartResourceWithRawResponse,
    VolumeChartResourceWithStreamingResponse,
    AsyncVolumeChartResourceWithStreamingResponse,
)

class AsyncExchangesResourceWithStreamingResponse:
    def __init__(self, exchanges: AsyncExchangesResource) -> None:
        self._exchanges = exchanges

        self.get = async_to_streamed_response_wrapper(
            exchanges.get,
        )
        self.get_id = async_to_streamed_response_wrapper(
            exchanges.get_id,
        )
        self.get_list = async_to_streamed_response_wrapper(
            exchanges.get_list,
        )

    @cached_property
    def tickers(self) -> AsyncTickersResourceWithStreamingResponse:
        return AsyncTickersResourceWithStreamingResponse(self._exchanges.tickers)

    @cached_property
    def volume_chart(self) -> AsyncVolumeChartResourceWithStreamingResponse:
        return AsyncVolumeChartResourceWithStreamingResponse(self._exchanges.volume_chart)