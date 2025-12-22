from functools import cached_property

class AsyncExchangesResourceWithStreamingResponse:
    """
    A wrapper around :class:`AsyncExchangesResource` that provides streaming
    responses for its sub‑resources.
    """

    def __init__(self, exchanges: "AsyncExchangesResource") -> None:
        # Store the underlying client and resource for later use.
        self._client = exchanges._client
        self._resource = exchanges

    @cached_property
    def tickers(self) -> "AsyncTickersResourceWithStreamingResponse":
        """
        Return a streaming wrapper for the ``tickers`` sub‑resource.
        """
        return AsyncTickersResourceWithStreamingResponse(
            self._client, self._resource.tickers
        )

    @cached_property
    def volume_chart(self) -> "AsyncVolumeChartResourceWithStreamingResponse":
        """
        Return a streaming wrapper for the ``volume_chart`` sub‑resource.
        """
        return AsyncVolumeChartResourceWithStreamingResponse(
            self._client, self._resource.volume_chart
        )