class AsyncAudioBatchIterator:
    """Async iterator for batch audio streaming."""

    def __init__(self, streamer: "AsyncAudioStreamer"):
        self._streamer = streamer
        # Default batch size is 1 if not provided by the streamer
        self._batch_size = getattr(streamer, "batch_size", 1)
        self._buffer = []

    def __aiter__(self):
        return self

    async def __anext__(self):
        # Keep fetching until we have a full batch or the streamer ends
        while len(self._buffer) < self._batch_size:
            try:
                chunk = await self._streamer.__anext__()
            except StopAsyncIteration:
                break
            self._buffer.append(chunk)

        if not self._buffer:
            raise StopAsyncIteration

        batch = self._buffer
        self._buffer = []
        return batch