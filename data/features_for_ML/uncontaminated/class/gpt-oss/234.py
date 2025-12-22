from __future__ import annotations
from typing import Any, Optional


class Skip:
    """Indicates that this was intentionally skipped."""

    def __init__(self, message: str | None = None, location: str | None = None):
        self.message: Optional[str] = message
        self.location: Optional[str] = location

    def combine(self, other: Any) -> Any:
        """
        Combine this Skip with another Outcome.

        If the other outcome is also a Skip, merge their messages and locations.
        Otherwise, the other outcome takes precedence (e.g., a failure overrides a skip).
        """
        if isinstance(other, Skip):
            # Merge messages
            if self.message and other.message:
                merged_message = f"{self.message}; {other.message}"
            else:
                merged_message = self.message or other.message

            # Merge location: prefer the more specific one
            merged_location = self.location or other.location

            return Skip(merged_message, merged_location)
        # If other is not a Skip, let it override
        return other

    def __str__(self) -> str:
        parts = ["Skipped"]
        if self.message:
            parts.append(f": {self.message}")
        if self.location:
            parts.append(f" ({self.location})")
        return "".join(parts)