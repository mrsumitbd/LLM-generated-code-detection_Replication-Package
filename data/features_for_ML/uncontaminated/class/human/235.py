from typing import Any

class AnalysisStep:
    """Represents an analysis step with sub-events."""

    step_count: int
    status: str | None = None
    method: str | None = None
    url: str | None = None
    queries: dict[str, Any] | None = None
    data: Any | None = None
    reason: str | None = None
    sub_events: list[LogEvent] = None

    def __post_init__(self):
        if self.sub_events is None:
            self.sub_events = []