class WorkflowExecutionResult:
    def __init__(self, status, workflow_id, outputs, step_outputs, inputs, error=None):
        self.status = status
        self.workflow_id = workflow_id
        self.outputs = outputs
        self.step_outputs = step_outputs
        self.inputs = inputs
        self.error = error