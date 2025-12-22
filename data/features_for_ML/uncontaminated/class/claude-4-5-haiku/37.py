class WorkflowRun:
    """Immutable data transfer object for workflow context.

    This DTO safely passes workflow context data between components without
    creating tight coupling or state conflicts.
    """

    def __init__(self, workflow_id: str, run_id: str, status: str, 
                 context: dict = None, metadata: dict = None):
        """Initialize a WorkflowRun instance.
        
        Args:
            workflow_id: Unique identifier for the workflow
            run_id: Unique identifier for this run
            status: Current status of the workflow run
            context: Optional workflow context data
            metadata: Optional metadata about the run
        """
        self._workflow_id = workflow_id
        self._run_id = run_id
        self._status = status
        self._context = dict(context) if context else {}
        self._metadata = dict(metadata) if metadata else {}

    @property
    def workflow_id(self) -> str:
        """Get the workflow ID."""
        return self._workflow_id

    @property
    def run_id(self) -> str:
        """Get the run ID."""
        return self._run_id

    @property
    def status(self) -> str:
        """Get the current status."""
        return self._status

    @property
    def context(self) -> dict:
        """Get a copy of the context data."""
        return dict(self._context)

    @property
    def metadata(self) -> dict:
        """Get a copy of the metadata."""
        return dict(self._metadata)

    def __repr__(self) -> str:
        """Return string representation of WorkflowRun."""
        return (f"WorkflowRun(workflow_id={self._workflow_id!r}, "
                f"run_id={self._run_id!r}, status={self._status!r})")

    def __eq__(self, other) -> bool:
        """Check equality with another WorkflowRun."""
        if not isinstance(other, WorkflowRun):
            return NotImplemented
        return (self._workflow_id == other._workflow_id and
                self._run_id == other._run_id and
                self._status == other._status and
                self._context == other._context and
                self._metadata == other._metadata)

    def __hash__(self) -> int:
        """Return hash of WorkflowRun."""
        return hash((self._workflow_id, self._run_id, self._status))