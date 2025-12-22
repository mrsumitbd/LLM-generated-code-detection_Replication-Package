class AsyncInfoResourceWithRawResponse:

    def __init__(self, info: AsyncInfoResource) -> None:
        self._info = info

    @property
    def retrieve(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return self._info.retrieve