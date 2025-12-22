class BaseTask:
    """Base class for evaluation tasks."""

    @property
    def name(self) -> str:
        return "Base Task"

    def get_task_instruction(self) -> str:
        return "This is a base task. Please implement specific instructions in subclasses."