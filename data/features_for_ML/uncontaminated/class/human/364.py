from typing import Any, Optional

class ExecutionState:
    """Represents the current execution state of a workflow"""

    workflow_id: str
    current_step_id: str | None = None
    inputs: dict[str, Any] = None
    step_outputs: dict[str, dict[str, Any]] = None
    workflow_outputs: dict[str, Any] = None
    dependency_outputs: dict[str, dict[str, Any]] = None
    status: dict[str, StepStatus] = None
    runtime_params: Optional["RuntimeParams"] = None

    def __post_init__(self):
        """Initialize default values"""
        if self.inputs is None:
            self.inputs = {}
        if self.step_outputs is None:
            self.step_outputs = {}
        if self.workflow_outputs is None:
            self.workflow_outputs = {}
        if self.dependency_outputs is None:
            self.dependency_outputs = {}
        if self.status is None:
            self.status = {}