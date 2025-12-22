from dataclasses import dataclass, field
from typing import List

@dataclass
class AnalysisStep:
    """Represents an analysis step with sub-events."""
    name: str
    sub_events: List[str] = field(default_factory=list)
    completed_sub_events: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.sub_events = sorted(self.sub_events)

    def add_sub_event(self, sub_event: str):
        self.sub_events.append(sub_event)
        self.sub_events = sorted(self.sub_events)

    def complete_sub_event(self, sub_event: str):
        if sub_event in self.sub_events:
            self.completed_sub_events.append(sub_event)
            self.sub_events.remove(sub_event)

    @property
    def is_complete(self) -> bool:
        return len(self.sub_events) == 0