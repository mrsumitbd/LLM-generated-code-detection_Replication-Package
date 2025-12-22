import anthropic
from dataclasses import dataclass


@dataclass
class RolloutEnvState:
    """Per-environment variables for the rollout loop."""
    
    client: anthropic.Anthropic
    model: str
    env_id: int
    max_steps: int
    system_prompt: str
    tools: list
    messages: list
    step_count: int = 0
    done: bool = False
    
    def reset(self):
        """Reset the environment state for a new episode."""
        self.messages = []
        self.step_count = 0
        self.done = False
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.messages.append({
            "role": role,
            "content": content
        })
    
    def get_messages(self) -> list:
        """Get the current message history."""
        return self.messages
    
    def increment_step(self):
        """Increment the step counter."""
        self.step_count += 1
        if self.step_count >= self.max_steps:
            self.done = True
    
    def is_done(self) -> bool:
        """Check if the episode is done."""
        return self.done
    
    def set_done(self, done: bool = True):
        """Set the done flag."""
        self.done = done