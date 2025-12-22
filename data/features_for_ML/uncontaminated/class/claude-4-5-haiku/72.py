class TopHoldersResourceWithStreamingResponse:

    def __init__(self, top_holders: TopHoldersResource) -> None:
        self._top_holders = top_holders

    @property
    def list(self) -> Callable[..., StreamingBytesIO]:
        return self._top_holders.list