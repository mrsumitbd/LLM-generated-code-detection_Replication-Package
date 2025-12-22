class AsyncPingResourceWithRawResponse:
    def __init__(self, ping: AsyncPingResource) -> None:
        self._ping = ping

    def __getattr__(self, name: str):
        return getattr(self._ping, name)