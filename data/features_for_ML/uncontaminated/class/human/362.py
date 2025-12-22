from .trending import (
    TrendingResource,
    AsyncTrendingResource,
    TrendingResourceWithRawResponse,
    AsyncTrendingResourceWithRawResponse,
    TrendingResourceWithStreamingResponse,
    AsyncTrendingResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.get = async_to_raw_response_wrapper(
            search.get,
        )

    @cached_property
    def trending(self) -> AsyncTrendingResourceWithRawResponse:
        return AsyncTrendingResourceWithRawResponse(self._search.trending)