class AsyncTrendingSearchResourceWithStreamingResponse:

    def __init__(self, trending_search: AsyncTrendingSearchResource) -> None:
        self._trending_search = trending_search

    @property
    def list(self) -> Callable[..., AsyncPaginator[TrendingSearch, AsyncCursorPagePaginator]]:
        return self._trending_search.list