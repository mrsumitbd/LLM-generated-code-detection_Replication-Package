import concurrent.futures
from typing import Any

class ParallelExecutor:
    """Execute tasks in parallel."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def run_tasks(self, tasks: list[Any]) -> list[Any]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(lambda task: task(), tasks)
        return list(results)