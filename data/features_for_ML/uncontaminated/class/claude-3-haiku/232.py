class AsyncAutoscaleResourceWithStreamingResponse:
    def __init__(self, autoscale: AsyncAutoscaleResource) -> None:
        self._autoscale = autoscale
        self._stream_response = None

    async def start_streaming(self) -> AsyncIterator[Any]:
        self._stream_response = await self._autoscale.start_streaming()
        async for item in self._stream_response:
            yield item

    async def stop_streaming(self) -> None:
        if self._stream_response:
            await self._stream_response.aclose()
            self._stream_response = None

    async def get_resource(self) -> AsyncAutoscaleResource:
        return self._autoscale

    async def __aenter__(self) -> "AsyncAutoscaleResourceWithStreamingResponse":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.stop_streaming()