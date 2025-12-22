from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncTrendingSearchResourceWithStreamingResponse:
    def __init__(self, trending_search: AsyncTrendingSearchResource) -> None:
        self._trending_search = trending_search

        self.get = async_to_streamed_response_wrapper(
            trending_search.get,
        )