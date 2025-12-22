from .actions import (
    ActionsResource,
    AsyncActionsResource,
    ActionsResourceWithRawResponse,
    AsyncActionsResourceWithRawResponse,
    ActionsResourceWithStreamingResponse,
    AsyncActionsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class ImagesResourceWithStreamingResponse:
    def __init__(self, images: ImagesResource) -> None:
        self._images = images

        self.create = to_streamed_response_wrapper(
            images.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            images.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            images.update,
        )
        self.list = to_streamed_response_wrapper(
            images.list,
        )
        self.delete = to_streamed_response_wrapper(
            images.delete,
        )

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self._images.actions)