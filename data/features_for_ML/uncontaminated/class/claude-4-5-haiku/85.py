class AsyncOhlcvResourceWithStreamingResponse:

    def __init__(self, ohlcv: AsyncOhlcvResource) -> None:
        self._ohlcv = ohlcv

    def __getattr__(self, name: str):
        base_method = getattr(self._ohlcv, name)
        
        async def streaming_wrapper(*args, **kwargs):
            result = await base_method(*args, **kwargs)
            return result
        
        if callable(base_method):
            return streaming_wrapper
        return base_method