from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, Optional


class ProbeResult:
    """
    A simple container for the result of a probe operation.

    Attributes
    ----------
    success : bool
        Indicates whether the probe succeeded.
    data : dict
        Arbitrary key/value data collected by the probe.
    error : Optional[str]
        Human‑readable error message if the probe failed.
    timestamp : datetime
        UTC timestamp when the result was created.
    """

    def __init__(
        self,
        success: bool = False,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        self.success: bool = success
        self.data: Dict[str, Any] = data or {}
        self.error: Optional[str] = error
        self.timestamp: datetime = datetime.utcnow()

    # ------------------------------------------------------------------
    # Mutator helpers
    # ------------------------------------------------------------------
    def set_success(self, success: bool) -> None:
        """Set the success flag."""
        self.success = success

    def add_data(self, key: str, value: Any) -> None:
        """Add a key/value pair to the data dictionary."""
        self.data[key] = value

    def set_error(self, error: str) -> None:
        """Set an error message."""
        self.error = error

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp.isoformat() + "Z",
        }

    def __repr__(self) -> str:
        return (
            f"ProbeResult(success={self.success!r}, "
            f"data={self.data!r}, error={self.error!r}, "
            f"timestamp={self.timestamp.isoformat()!r})"
        )

    def __str__(self) -> str:
        """Return a JSON string representation."""
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)