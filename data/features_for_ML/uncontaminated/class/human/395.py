import asyncio

class AsyncAudioBatchIterator:
    """Async iterator for batch audio streaming."""
    
    def __init__(self, streamer: AsyncAudioStreamer):
        self.streamer = streamer
        self.active_samples = set(range(streamer.batch_size))
        
    def __aiter__(self):
        return self
        
    async def __anext__(self):
        if not self.active_samples:
            raise StopAsyncIteration()
            
        batch_chunks = {}
        samples_to_remove = set()
        
        # Create tasks for all active samples
        tasks = {
            idx: asyncio.create_task(self._get_chunk(idx)) 
            for idx in self.active_samples
        }
        
        # Wait for at least one chunk to be ready
        done, pending = await asyncio.wait(
            tasks.values(), 
            return_when=asyncio.FIRST_COMPLETED,
            timeout=self.streamer.timeout
        )
        
        # Cancel pending tasks
        for task in pending:
            task.cancel()
            
        # Process completed tasks
        for idx, task in tasks.items():
            if task in done:
                try:
                    value = await task
                    if value == self.streamer.stop_signal:
                        samples_to_remove.add(idx)
                    else:
                        batch_chunks[idx] = value
                except asyncio.CancelledError:
                    pass
                    
        self.active_samples -= samples_to_remove
        
        if batch_chunks:
            return batch_chunks
        elif self.active_samples:
            # Try again if we still have active samples
            return await self.__anext__()
        else:
            raise StopAsyncIteration()
    
    async def _get_chunk(self, idx):
        """Helper to get a chunk from a specific queue."""
        return await self.streamer.audio_queues[idx].get()