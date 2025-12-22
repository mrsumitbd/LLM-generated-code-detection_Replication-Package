from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, Mapping, MutableMapping


@dataclass
class WorkflowExecutionResult:
    """
    Represents the result of a workflow execution.

    This class models the structure of the result returned by the
    `execute_workflow` method.

    Attributes:
        status: The status of the workflow execution (e.g., WORKFLOW_COMPLETE, ERROR)
        workflow_id: The ID of the executed workflow
        outputs: The outputs produced by the workflow
        step_outputs: The outputs from each step in the workflow
        inputs: The original inputs provided to the workflow
        error: Optional error message if the workflow execution failed
    """

    status: str
    workflow_id: str
    outputs: MutableMapping[str, Any] = field(default_factory=dict)
    step_outputs: MutableMapping[str, MutableMapping[str, Any]] = field(default_factory=dict)
    inputs: MutableMapping[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def __post_init__(self) -> None:
        # Ensure that step_outputs is a mapping of mappings
        for step, out in self.step_outputs.items():
            if not isinstance(out, Mapping):
                raise TypeError(
                    f"step_outputs[{step!r}] must be a mapping, got {type(out).__name__}"
                )

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def is_successful(self) -> bool:
        """Return True if the workflow completed successfully."""
        return self.status.upper() == "WORKFLOW_COMPLETE"

    def add_step_output(self, step_name: str, key: str, value: Any) -> None:
        """Add an output value for a specific step."""
        if step_name not in self.step_outputs:
            self.step_outputs[step_name] = {}
        self.step_outputs[step_name][key] = value

    def get_step_output(self, step_name: str, key: str) -> Any:
        """Retrieve a specific output from a step."""
        return self.step_outputs.get(step_name, {}).get(key)

    def get_output(self, key: str) -> Any:
        """Retrieve a top‑level output value."""
        return self.outputs.get(key)

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dictionary representation of the result."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkflowExecutionResult":
        """Create an instance from a dictionary."""
        return cls(
            status=data.get("status", ""),
            workflow_id=data.get("workflow_id", ""),
            outputs=data.get("outputs", {}),
            step_outputs=data.get("step_outputs", {}),
            inputs=data.get("inputs", {}),
            error=data.get("error"),
        )

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return (
            f"{cls_name}(status={self.status!r}, workflow_id={self.workflow_id!r}, "
            f"outputs={self.outputs!r}, step_outputs={self.step_outputs!r}, "
            f"inputs={self.inputs!r}, error={self.error!r})"
        )