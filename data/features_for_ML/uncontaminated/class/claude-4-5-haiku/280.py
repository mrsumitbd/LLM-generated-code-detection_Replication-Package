from dataclasses import dataclass, field
from typing import List

@dataclass
class DebateAgent:
    """Represents a debate participant"""
    
    name: str = ""
    meta_prompt: str = ""
    events: List[str] = field(default_factory=list)
    memories: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.events:
            self.events = []
        if not self.memories:
            self.memories = []

    def set_meta_prompt(self, meta_prompt: str):
        self.meta_prompt = meta_prompt

    def add_event(self, event: str):
        self.events.append(event)

    def add_memory(self, memory: str):
        self.memories.append(memory)