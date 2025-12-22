class AsyncFunctionsResourceWithRawResponse:

    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self._functions = functions

    @property
    def list(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._functions.list

    @property
    def retrieve(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._functions.retrieve

    @property
    def create(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._functions.create

    @property
    def update(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._functions.update

    @property
    def delete(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._functions.delete