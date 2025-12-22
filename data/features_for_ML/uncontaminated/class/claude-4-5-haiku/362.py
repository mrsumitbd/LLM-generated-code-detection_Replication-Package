class AsyncSearchResourceWithRawResponse:

    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

    @cached_property
    def trending(self) -> AsyncTrendingResourceWithRawResponse:
        return AsyncTrendingResourceWithRawResponse(self._search.trending)