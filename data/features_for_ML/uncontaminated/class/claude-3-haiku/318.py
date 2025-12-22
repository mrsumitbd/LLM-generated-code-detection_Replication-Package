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
        self.status = status
        self.workflow_id = workflow_id
        self.outputs = outputs
        self.step_outputs = step_outputs
        self.inputs = inputs
        self.error = error