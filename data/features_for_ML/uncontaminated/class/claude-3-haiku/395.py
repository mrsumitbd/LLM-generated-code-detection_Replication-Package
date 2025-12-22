import asyncio

class AsyncAudioBatchIterator:
    """Async iterator for batch audio streaming."""

    def __init__(self, streamer: AsyncAudioStreamer):
        self.streamer = streamer
        self.batch_size = streamer.batch_size
        self.buffer = []
        self.is_exhausted = False

    async def __aiter__(self):
        return self

    async def __anext__(self):
        if self.is_exhausted:
            raise StopAsyncIteration

        while len(self.buffer) < self.batch_size:
            try:
                audio_data = await self.streamer.read()
                self.buffer.append(audio_data)
            except asyncio.TimeoutError:
                self.is_exhausted = True
                break

        batch = self.buffer[:self.batch_size]
        self.buffer = self.buffer[self.batch_size:]
        return batch