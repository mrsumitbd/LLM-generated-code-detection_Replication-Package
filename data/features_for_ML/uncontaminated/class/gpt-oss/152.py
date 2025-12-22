class BaseTask:
    """Base class for evaluation tasks."""

    @property
    def name(self) -> str:
        """Return the name of the task."""
        raise NotImplementedError("Subclasses must implement the 'name' property.")

    def get_task_instruction(self) -> str:
        """Return the instruction string for the task."""
        raise NotImplementedError("Subclasses must implement 'get_task_instruction'.")