from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncAutoscaleResourceWithStreamingResponse:
    def __init__(self, autoscale: AsyncAutoscaleResource) -> None:
        self._autoscale = autoscale

        self.create = async_to_streamed_response_wrapper(
            autoscale.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            autoscale.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            autoscale.update,
        )
        self.list = async_to_streamed_response_wrapper(
            autoscale.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            autoscale.delete,
        )
        self.delete_dangerous = async_to_streamed_response_wrapper(
            autoscale.delete_dangerous,
        )
        self.list_history = async_to_streamed_response_wrapper(
            autoscale.list_history,
        )
        self.list_members = async_to_streamed_response_wrapper(
            autoscale.list_members,
        )