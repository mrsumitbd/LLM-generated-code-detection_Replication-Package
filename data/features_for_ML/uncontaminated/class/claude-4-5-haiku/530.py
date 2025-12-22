class AsyncPingResourceWithRawResponse:

    def __init__(self, ping: AsyncPingResource) -> None:
        self._ping = ping

    @property
    def ping(self) -> AsyncPingResourceWithRawResponse:
        return AsyncPingResourceWithRawResponse(self._ping)