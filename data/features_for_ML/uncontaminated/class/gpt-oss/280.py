from dataclasses import dataclass, field
from typing import List


@dataclass
class DebateAgent:
    """Represents a debate participant."""

    meta_prompt: str = ""
    events: List[str] = field(default_factory=list)
    memory: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Ensure that events and memory are always lists
        if self.events is None:
            self.events = []
        if self.memory is None:
            self.memory = []

    def set_meta_prompt(self, meta_prompt: str):
        """Set the meta prompt for the agent."""
        self.meta_prompt = meta_prompt

    def add_event(self, event: str):
        """Add an event to the agent's event history."""
        self.events.append(event)

    def add_memory(self, memory: str):
        """Add a memory entry to the agent's memory."""
        self.memory.append(memory)