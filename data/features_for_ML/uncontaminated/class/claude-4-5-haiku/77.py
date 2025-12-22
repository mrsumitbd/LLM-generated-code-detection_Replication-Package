class ImagesResourceWithStreamingResponse:

    def __init__(self, images: ImagesResource) -> None:
        self._images = images

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self._images.actions)