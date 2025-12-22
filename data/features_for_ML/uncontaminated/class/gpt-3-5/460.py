import asyncio

class AsyncFuzzExecutor:
    """Executes fuzzing operations asynchronously with controlled concurrency."""

    def __init__(self, max_concurrency: int = 5):
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)

    def _get_semaphore(self):
        return self.semaphore