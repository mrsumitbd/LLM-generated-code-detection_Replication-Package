class AsyncModelsResourceWithRawResponse:

    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

    @property
    def list(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._models.list

    @property
    def retrieve(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._models.retrieve

    @property
    def delete(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._models.delete