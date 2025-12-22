from __future__ import annotations

import copy
import datetime
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class AIRAState:
    """
    State object for AIRA LangGraph workflow.

    The state tracks user/session identifiers, a mutable context dictionary,
    arbitrary variables, a history of executed steps, and timestamps for
    creation and last update.  It provides convenient helpers for
    serialization, cloning, and step management.
    """

    # Core identifiers
    user_id: str
    session_id: str

    # Mutable context and variables
    context: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)

    # History of executed steps
    step_history: List[Dict[str, Any]] = field(default_factory=list)

    # Timestamps
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)

    # ------------------------------------------------------------------
    # Basic state manipulation
    # ------------------------------------------------------------------
    def update_context(self, key: str, value: Any) -> None:
        """Set a key/value pair in the context dictionary."""
        self.context[key] = value
        self._touch()

    def get_context(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the context dictionary."""
        return self.context.get(key, default)

    def add_variable(self, key: str, value: Any) -> None:
        """Add or update a variable."""
        self.variables[key] = value
        self._touch()

    def get_variable(self, key: str, default: Any = None) -> Any:
        """Retrieve a variable value."""
        return self.variables.get(key, default)

    # ------------------------------------------------------------------
    # Step history management
    # ------------------------------------------------------------------
    def add_step(
        self,
        step_name: str,
        input_data: Any = None,
        output_data: Any = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record a step execution.

        Parameters
        ----------
        step_name : str
            Identifier for the step.
        input_data : Any, optional
            Data fed into the step.
        output_data : Any, optional
            Result produced by the step.
        metadata : dict, optional
            Additional information (e.g., timestamps, status).
        """
        step_record = {
            "step_name": step_name,
            "input": input_data,
            "output": output_data,
            "metadata": metadata or {},
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
        self.step_history.append(step_record)
        self._touch()

    def clear_history(self) -> None:
        """Remove all recorded steps."""
        self.step_history.clear()
        self._touch()

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dictionary representation of the state."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AIRAState":
        """Create a state instance from a dictionary."""
        # Convert timestamps from ISO strings if present
        for ts_field in ("created_at", "updated_at"):
            if ts_field in data and isinstance(data[ts_field], str):
                data[ts_field] = datetime.datetime.fromisoformat(data[ts_field])
        return cls(**data)

    def to_json(self, *, indent: Optional[int] = None) -> str:
        """Serialize the state to a JSON string."""
        def default(o):
            if isinstance(o, datetime.datetime):
                return o.isoformat()
            raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

        return json.dumps(self.to_dict(), default=default, indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "AIRAState":
        """Deserialize a JSON string into a state instance."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def clone(self) -> "AIRAState":
        """Return a deep copy of the state."""
        return copy.deepcopy(self)

    def _touch(self) -> None:
        """Update the `updated_at` timestamp."""
        self.updated_at = datetime.datetime.utcnow()

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(user_id={self.user_id!r}, "
            f"session_id={self.session_id!r}, "
            f"context_keys={list(self.context.keys())!r}, "
            f"variables_keys={list(self.variables.keys())!r}, "
            f"steps={len(self.step_history)})"
        )