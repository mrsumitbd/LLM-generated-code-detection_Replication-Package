class AsyncAudioBatchIterator:
    """Async iterator for batch audio streaming."""

    def __init__(self, streamer: AsyncAudioStreamer):
        self.streamer = streamer

    async def __aiter__(self):
        return self

    async def __anext__(self):
        batch = await self.streamer.get_next_batch()
        if batch is None:
            raise StopAsyncIteration
        return batch