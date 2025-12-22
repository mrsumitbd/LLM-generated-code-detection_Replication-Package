from functools import cached_property

class AsyncSearchResourceWithRawResponse:
    """
    Wrapper around :class:`AsyncSearchResource` that exposes raw HTTP responses.
    """

    def __init__(self, search: "AsyncSearchResource") -> None:
        """
        Initialize the wrapper.

        Parameters
        ----------
        search : AsyncSearchResource
            The underlying async search resource.
        """
        self._search = search

    @cached_property
    def trending(self) -> "AsyncTrendingResourceWithRawResponse":
        """
        Return a wrapper around the trending resource that exposes raw responses.

        Returns
        -------
        AsyncTrendingResourceWithRawResponse
            The wrapped trending resource.
        """
        from .trending import AsyncTrendingResourceWithRawResponse  # local import to avoid circular deps
        return AsyncTrendingResourceWithRawResponse(self._search.trending)