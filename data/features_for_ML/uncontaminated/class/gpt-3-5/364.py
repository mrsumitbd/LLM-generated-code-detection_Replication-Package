class ExecutionState:
    """Represents the current execution state of a workflow"""

    def __post_init__(self):
        self.workflow_id = None
        self.current_step = None
        self.status = "Pending"
        self.output = {}

    def set_workflow_id(self, workflow_id):
        self.workflow_id = workflow_id

    def set_current_step(self, current_step):
        self.current_step = current_step

    def set_status(self, status):
        self.status = status

    def set_output(self, output):
        self.output = output

    def get_workflow_id(self):
        return self.workflow_id

    def get_current_step(self):
        return self.current_step

    def get_status(self):
        return self.status

    def get_output(self):
        return self.output