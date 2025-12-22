import time
from typing import Any, Dict, Optional


class CachedMeeting:
    """Cached meeting information with expiration."""

    def __init__(
        self,
        meeting_id: str,
        data: Dict[str, Any],
        ttl_seconds: int = 300,
        *,
        created_at: Optional[float] = None,
    ) -> None:
        """
        Initialize a CachedMeeting.

        Parameters
        ----------
        meeting_id : str
            Unique identifier for the meeting.
        data : dict
            Arbitrary meeting data to cache.
        ttl_seconds : int, optional
            Time-to-live in seconds. Defaults to 300 (5 minutes).
        created_at : float, optional
            Unix timestamp when the cache was created. If None, current time is used.
        """
        self.meeting_id = meeting_id
        self._data = data
        self.ttl_seconds = ttl_seconds
        self.created_at = created_at if created_at is not None else time.time()

    @property
    def is_expired(self) -> bool:
        """Return True if the cached meeting has expired."""
        return (time.time() - self.created_at) > self.ttl_seconds

    @property
    def remaining_ttl(self) -> float:
        """Return remaining time-to-live in seconds. Negative if expired."""
        return self.ttl_seconds - (time.time() - self.created_at)

    def refresh(self, new_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Refresh the cached meeting.

        Parameters
        ----------
        new_data : dict, optional
            New data to replace the existing cache. If None, only the timestamp is updated.
        """
        if new_data is not None:
            self._data = new_data
        self.created_at = time.time()

    def get_data(self) -> Dict[str, Any]:
        """Return the cached meeting data."""
        return self._data

    def __repr__(self) -> str:
        status = "expired" if self.is_expired else "valid"
        return (
            f"<CachedMeeting id={self.meeting_id!r} status={status} "
            f"ttl={self.ttl_seconds}s remaining={self.remaining_ttl:.1f}s>"
        )