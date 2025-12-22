from typing import List

class EvaluationRemoteWorkflowHandler:

    def __init__(self, config: EvaluationRunConfig, max_concurrency: int):
        self.config = config
        self.max_concurrency = max_concurrency
        self.running_tasks = []

    def start_workflow(self):
        pass

    def stop_workflow(self):
        pass

    def _execute_task(self, task_id: int):
        pass

class EvaluationRunConfig:
    def __init__(self, tasks: List[str]):
        self.tasks = tasks