from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class ExecutionState:
    """Represents the current execution state of a workflow"""

    # Workflow status: e.g., "pending", "running", "completed", "failed"
    status: str = "pending"

    # Timestamp when the workflow started
    start_time: Optional[datetime] = None

    # Timestamp when the workflow finished (if applicable)
    end_time: Optional[datetime] = None

    # Name or identifier of the current step being executed
    current_step: Optional[str] = None

    # Dictionary of variables or context data available to the workflow
    variables: Dict[str, Any] = field(default_factory=dict)

    # List of error messages encountered during execution
    errors: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize default values and validate state."""
        # Ensure status is a string
        if not isinstance(self.status, str):
            raise TypeError("status must be a string")

        # If start_time is not provided, set it to now
        if self.start_time is None:
            self.start_time = datetime.utcnow()

        # Validate timestamps
        if self.end_time is not None and self.end_time < self.start_time:
            raise ValueError("end_time cannot be earlier than start_time")

        # Ensure variables is a dict
        if not isinstance(self.variables, dict):
            raise TypeError("variables must be a dictionary")

        # Ensure errors is a list
        if not isinstance(self.errors, list):
            raise TypeError("errors must be a list")

    # Convenience methods for state manipulation

    def start(self, step: Optional[str] = None) -> None:
        """Mark the workflow as running and optionally set the current step."""
        self.status = "running"
        self.start_time = datetime.utcnow()
        if step:
            self.current_step = step

    def complete(self, step: Optional[str] = None) -> None:
        """Mark the workflow as completed."""
        self.status = "completed"
        self.end_time = datetime.utcnow()
        if step:
            self.current_step = step

    def fail(self, error: str, step: Optional[str] = None) -> None:
        """Mark the workflow as failed and record an error."""
        self.status = "failed"
        self.end_time = datetime.utcnow()
        self.errors.append(error)
        if step:
            self.current_step = step

    def set_variable(self, key: str, value: Any) -> None:
        """Set a variable in the workflow context."""
        self.variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        """Retrieve a variable from the workflow context."""
        return self.variables.get(key, default)

    def add_error(self, error: str) -> None:
        """Add an error message to the error list."""
        self.errors.append(error)

    def __repr__(self) -> str:
        return (
            f"ExecutionState(status={self.status!r}, "
            f"start_time={self.start_time!r}, end_time={self.end_time!r}, "
            f"current_step={self.current_step!r}, variables={self.variables!r}, "
            f"errors={self.errors!r})"
        )