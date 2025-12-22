from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Iterable, List


class ParallelExecutor:
    """Execute tasks in parallel."""

    def __init__(self, max_workers: int = 4):
        """
        Initialize the executor with a maximum number of worker threads.

        Parameters
        ----------
        max_workers : int, optional
            The maximum number of threads to use for parallel execution.
            Defaults to 4.
        """
        self.max_workers = max_workers

    def run_tasks(self, tasks: Iterable[Callable[[], Any]]) -> List[Any]:
        """
        Execute a collection of callables concurrently and return their results.

        Parameters
        ----------
        tasks : Iterable[Callable[[], Any]]
            An iterable of zero‑argument callables. Each callable will be
            executed in a separate thread (up to ``max_workers``).

        Returns
        -------
        List[Any]
            A list containing the return values of the callables, in the same
            order as the input iterable.

        Raises
        ------
        Exception
            Any exception raised by a task is propagated to the caller.
        """
        results: List[Any] = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks and keep the futures in order
            futures = [executor.submit(task) for task in tasks]

            # Retrieve results in the order of submission
            for future in futures:
                results.append(future.result())

        return results