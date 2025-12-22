class AsyncCategoriesResourceWithRawResponse:

    def __init__(self, categories: AsyncCategoriesResource) -> None:
        self._categories = categories

    @property
    def list(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._categories.list

    @property
    def retrieve(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._categories.retrieve

    @property
    def with_raw_response(self) -> AsyncCategoriesResourceWithRawResponse:
        return self

    @property
    def with_streaming_response(self) -> AsyncCategoriesResourceWithStreamingResponse:
        return AsyncCategoriesResourceWithStreamingResponse(self._categories)