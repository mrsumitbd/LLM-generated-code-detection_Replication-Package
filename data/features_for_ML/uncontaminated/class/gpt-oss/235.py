from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable, List, Iterator


@dataclass
class AnalysisStep:
    """Represents an analysis step with sub-events."""
    name: str
    description: str = ""
    sub_events: List[Any] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.sub_events is None:
            self.sub_events = []

    def add_sub_event(self, event: Any) -> None:
        """Add a sub-event to the step."""
        self.sub_events.append(event)

    def remove_sub_event(self, event: Any) -> None:
        """Remove a sub-event from the step."""
        self.sub_events.remove(event)

    def clear_sub_events(self) -> None:
        """Remove all sub-events."""
        self.sub_events.clear()

    def __len__(self) -> int:
        return len(self.sub_events)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.sub_events)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name!r}, "
            f"description={self.description!r}, "
            f"sub_events={self.sub_events!r})"
        )