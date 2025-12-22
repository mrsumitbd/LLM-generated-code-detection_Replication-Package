from datetime import UTC, datetime

class SessionData:
    """Data entry for a terminal session."""

    timestamp: datetime
    source: str  # "user" or "command"
    content: str