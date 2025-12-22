import asyncio
from typing import Awaitable, Iterable, List, Any, Callable, Coroutine


class AsyncFuzzExecutor:
    """Executes fuzzing operations asynchronously with controlled concurrency."""

    def __init__(self, max_concurrency: int = 5):
        """
        Initialize the executor.

        Parameters
        ----------
        max_concurrency : int, optional
            Maximum number of concurrent fuzzing tasks. Defaults to 5.
        """
        if max_concurrency <= 0:
            raise ValueError("max_concurrency must be a positive integer")
        self._max_concurrency: int = max_concurrency
        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(max_concurrency)
        self._tasks: List[asyncio.Task] = []

    def _get_semaphore(self) -> asyncio.Semaphore:
        """Return the internal semaphore used for concurrency control."""
        return self._semaphore

    async def _run_task(self, coro: Awaitable[Any]) -> Any:
        """Run a single coroutine with concurrency control."""
        async with self._semaphore:
            return await coro

    async def run(self, coro: Awaitable[Any]) -> asyncio.Task:
        """
        Schedule a coroutine to run with concurrency control.

        Parameters
        ----------
        coro : Awaitable[Any]
            The coroutine to execute.

        Returns
        -------
        asyncio.Task
            The task object representing the scheduled coroutine.
        """
        task = asyncio.create_task(self._run_task(coro))
        self._tasks.append(task)
        return task

    async def run_all(self, coros: Iterable[Awaitable[Any]]) -> List[Any]:
        """
        Run multiple coroutines concurrently with concurrency control.

        Parameters
        ----------
        coros : Iterable[Awaitable[Any]]
            An iterable of coroutines to execute.

        Returns
        -------
        List[Any]
            A list of results from the coroutines, in the same order.
        """
        tasks = [self.run(c) for c in coros]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results

    async def shutdown(self) -> None:
        """
        Wait for all scheduled tasks to complete.

        This method should be called before the executor is discarded.
        """
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
            self._tasks.clear()

    async def __aenter__(self) -> "AsyncFuzzExecutor":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.shutdown()