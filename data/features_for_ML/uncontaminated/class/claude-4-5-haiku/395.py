class AsyncAudioBatchIterator:
    """Async iterator for batch audio streaming."""

    def __init__(self, streamer: AsyncAudioStreamer):
        self.streamer = streamer
        self._batch = []
        self._finished = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._finished and not self._batch:
            raise StopAsyncIteration
        
        self._batch = []
        
        async for chunk in self.streamer:
            self._batch.append(chunk)
            if len(self._batch) >= self.streamer.batch_size:
                return self._batch
        
        self._finished = True
        
        if self._batch:
            return self._batch
        
        raise StopAsyncIteration