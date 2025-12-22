from typing import List, Dict, Any, Optional, Tuple, Set

class ErrorReport:
    """Information on a parsing failure."""

    error: str
    log: str
    location: Optional[str] = None
    recoverable: bool = True

    def __str__(self) -> str:
        """Format error for display."""
        location_str = f" at {self.location}" if self.location else ""
        recovery_str = " (recoverable)" if self.recoverable else " (fatal)"
        return (
            f"Error{location_str}: {self.error}{recovery_str}\nLog snippet: {self.log}"
        )