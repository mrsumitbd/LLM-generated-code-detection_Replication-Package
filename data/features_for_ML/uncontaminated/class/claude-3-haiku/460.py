import asyncio

class AsyncFuzzExecutor:
    """Executes fuzzing operations asynchronously with controlled concurrency."""

    def __init__(self, max_concurrency: int = 5):
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def _get_semaphore(self):
        async with self._semaphore:
            yield

    async def execute_fuzzing(self, fuzzing_task):
        async with self._get_semaphore():
            result = await fuzzing_task()
            return result

    async def execute_many_fuzzing(self, fuzzing_tasks):
        tasks = [self.execute_fuzzing(task) for task in fuzzing_tasks]
        return await asyncio.gather(*tasks)