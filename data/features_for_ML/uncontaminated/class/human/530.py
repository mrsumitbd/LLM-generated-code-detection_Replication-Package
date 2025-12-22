from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncPingResourceWithRawResponse:
    def __init__(self, ping: AsyncPingResource) -> None:
        self._ping = ping

        self.get = async_to_raw_response_wrapper(
            ping.get,
        )