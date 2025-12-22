import asyncio
from typing import Callable, Any, List
from concurrent.futures import ThreadPoolExecutor

class AsyncFuzzExecutor:
    """Executes fuzzing operations asynchronously with controlled concurrency."""

    def __init__(self, max_concurrency: int = 5):
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.thread_pool = ThreadPoolExecutor(max_workers=max_concurrency)

    def _get_semaphore(self):
        return self.semaphore

    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with semaphore-controlled concurrency."""
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.thread_pool, func, *args)

    async def execute_many(self, tasks: List[tuple]) -> List[Any]:
        """Execute multiple tasks concurrently with controlled concurrency."""
        coroutines = [self.execute(func, *args, **kwargs) 
                     for func, args, kwargs in tasks]
        return await asyncio.gather(*coroutines)

    def close(self):
        """Close the thread pool executor."""
        self.thread_pool.shutdown(wait=True)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()