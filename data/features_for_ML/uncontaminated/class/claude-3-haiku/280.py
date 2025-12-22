class DebateAgent:
    """Represents a debate participant"""

    def __init__(self):
        self.meta_prompt = None
        self.events = []
        self.memories = []

    def set_meta_prompt(self, meta_prompt: str):
        self.meta_prompt = meta_prompt

    def add_event(self, event: str):
        self.events.append(event)

    def add_memory(self, memory: str):
        self.memories.append(memory)