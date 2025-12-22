class WorkflowRun:
    def __init__(self, workflow_id, status, start_time, end_time, output):
        self._workflow_id = workflow_id
        self._status = status
        self._start_time = start_time
        self._end_time = end_time
        self._output = output

    @property
    def workflow_id(self):
        return self._workflow_id

    @property
    def status(self):
        return self._status

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def output(self):
        return self._output

    def __str__(self):
        return f"WorkflowRun(workflow_id={self.workflow_id}, status={self.status}, start_time={self.start_time}, end_time={self.end_time}, output={self.output})"