import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Any

class ParallelExecutor:
    """Execute tasks in parallel."""

    def __init__(self, max_workers: int = 4):
        """Initialize parallel executor."""
        self.max_workers = max_workers

    async def run_parallel(self, tasks: list[Any]) -> list[Any]:
        """Run tasks in parallel using asyncio."""
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    def run_tasks(self, tasks: list[Any]) -> list[Any]:
        """Run callable tasks in parallel using threads."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(task) for task in tasks]
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(e)
        return results