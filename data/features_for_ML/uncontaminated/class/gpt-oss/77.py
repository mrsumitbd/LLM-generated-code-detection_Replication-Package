from functools import cached_property

class ImagesResourceWithStreamingResponse:
    """
    A wrapper around an `ImagesResource` that provides streaming‑response
    capabilities for its sub‑resources.
    """

    def __init__(self, images: ImagesResource) -> None:
        """
        Initialize the wrapper with an existing `ImagesResource`.

        Parameters
        ----------
        images : ImagesResource
            The underlying images resource to wrap.
        """
        self._images = images

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        """
        Lazily create and return a streaming‑response wrapper for the
        `actions` sub‑resource of the underlying images resource.

        Returns
        -------
        ActionsResourceWithStreamingResponse
            A wrapper that streams responses for actions.
        """
        return ActionsResourceWithStreamingResponse(self._images.actions)