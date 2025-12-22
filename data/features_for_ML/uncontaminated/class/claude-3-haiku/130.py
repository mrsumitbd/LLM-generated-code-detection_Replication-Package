import concurrent.futures

class ParallelExecutor:
    """Execute tasks in parallel."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def run_tasks(self, tasks: list[Any]) -> list[Any]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(lambda task: task(), tasks))
        return results