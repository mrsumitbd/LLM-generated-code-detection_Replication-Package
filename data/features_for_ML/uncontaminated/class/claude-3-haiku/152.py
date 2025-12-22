class BaseTask:
    """Base class for evaluation tasks."""

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def get_task_instruction(self) -> str:
        return f"Complete the {self.name} task."