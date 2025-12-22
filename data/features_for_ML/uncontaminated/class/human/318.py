from dataclasses import dataclass, field
from typing import Any, Optional

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

    status: WorkflowExecutionStatus
    workflow_id: str
    outputs: dict[str, Any] = field(default_factory=dict)
    step_outputs: dict[str, dict[str, Any]] | None = None
    inputs: dict[str, Any] | None = None
    error: str | None = None