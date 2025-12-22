from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class TopHoldersResourceWithStreamingResponse:
    def __init__(self, top_holders: TopHoldersResource) -> None:
        self._top_holders = top_holders

        self.get = to_streamed_response_wrapper(
            top_holders.get,
        )