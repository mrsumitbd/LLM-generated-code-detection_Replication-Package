from functools import cached_property

class ImagesResourceWithStreamingResponse:

    def __init__(self, images: ImagesResource) -> None:
        self.images = images

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self.images)