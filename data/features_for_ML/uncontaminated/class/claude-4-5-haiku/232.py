class AsyncAutoscaleResourceWithStreamingResponse:

    def __init__(self, autoscale: AsyncAutoscaleResource) -> None:
        self._autoscale = autoscale

    def __getattr__(self, name: str):
        return getattr(self._autoscale, name)