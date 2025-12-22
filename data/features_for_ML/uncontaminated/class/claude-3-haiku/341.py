import concurrent.futures
import logging
import time

class EvaluationRemoteWorkflowHandler:
    def __init__(self, config: EvaluationRunConfig, max_concurrency: int):
        self.config = config
        self.max_concurrency = max_concurrency
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrency)
        self.futures = []

    def submit_evaluation(self, evaluation_task: EvaluationTask):
        future = self.executor.submit(self.execute_evaluation, evaluation_task)
        self.futures.append(future)

    def execute_evaluation(self, evaluation_task: EvaluationTask):
        try:
            evaluation_task.run()
        except Exception as e:
            logging.error(f"Error executing evaluation task: {e}")

    def wait_for_completion(self):
        concurrent.futures.wait(self.futures)
        self.executor.shutdown(wait=True)

    def cancel_all_tasks(self):
        for future in self.futures:
            future.cancel()
        self.executor.shutdown(wait=False)