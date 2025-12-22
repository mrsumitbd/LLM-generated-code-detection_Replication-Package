class WorkflowRun:
    """Immutable data transfer object for workflow context.

    This DTO safely passes workflow context data between components without
    creating tight coupling or state conflicts.
    """

    def __init__(self, workflow_id, run_id, inputs, outputs, status, created_at, updated_at):
        self._workflow_id = workflow_id
        self._run_id = run_id
        self._inputs = inputs
        self._outputs = outputs
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def workflow_id(self):
        return self._workflow_id

    @property
    def run_id(self):
        return self._run_id

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def status(self):
        return self._status

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at