class WorkflowExecutionResult:
    """Represents the result of a workflow execution

    This class models the structure of the result returned by the execute_workflow method.

    Attributes:
        status: The status of the workflow execution (e.g., WORKFLOW_COMPLETE, ERROR)
        workflow_id: The ID of the executed workflow
        outputs: The outputs produced by the workflow
        step_outputs: The outputs from each step in the workflow
        inputs: The original inputs provided to the workflow
        error: Optional error message if the workflow execution failed
    """

    def __init__(self, status, workflow_id, outputs, step_outputs, inputs, error=None):
        """Initialize a WorkflowExecutionResult.

        Args:
            status: The status of the workflow execution
            workflow_id: The ID of the executed workflow
            outputs: The outputs produced by the workflow
            step_outputs: The outputs from each step in the workflow
            inputs: The original inputs provided to the workflow
            error: Optional error message if the workflow execution failed
        """
        self.status = status
        self.workflow_id = workflow_id
        self.outputs = outputs
        self.step_outputs = step_outputs
        self.inputs = inputs
        self.error = error

    def __repr__(self):
        """Return a string representation of the WorkflowExecutionResult."""
        return (
            f"WorkflowExecutionResult(status={self.status!r}, "
            f"workflow_id={self.workflow_id!r}, outputs={self.outputs!r}, "
            f"step_outputs={self.step_outputs!r}, inputs={self.inputs!r}, "
            f"error={self.error!r})"
        )

    def __eq__(self, other):
        """Check equality between two WorkflowExecutionResult instances."""
        if not isinstance(other, WorkflowExecutionResult):
            return False
        return (
            self.status == other.status
            and self.workflow_id == other.workflow_id
            and self.outputs == other.outputs
            and self.step_outputs == other.step_outputs
            and self.inputs == other.inputs
            and self.error == other.error
        )