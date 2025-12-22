from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any


class ParallelExecutor:
    """Execute tasks in parallel."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def run_tasks(self, tasks: list[Any]) -> list[Any]:
        results = [None] * len(tasks)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {
                executor.submit(task): idx 
                for idx, task in enumerate(tasks)
            }
            
            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    results[idx] = e
        
        return results