import anthropic
from typing import Any


class MessageThread:
    """A simple message thread container."""
    def __init__(self):
        self.messages = []
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self):
        return self.messages


class ResearchAgent:

    def __init__(self, app: Any, thread: MessageThread):
        self.app = app
        self.thread = thread
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
    
    def research(self, query: str) -> str:
        """Conduct research on a given query using Claude."""
        self.thread.add_message("user", query)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system="You are a research assistant. Provide detailed, accurate, and well-researched responses to queries.",
            messages=self.thread.get_messages()
        )
        
        assistant_message = response.content[0].text
        self.thread.add_message("assistant", assistant_message)
        
        return assistant_message
    
    def get_thread_history(self) -> list:
        """Get the conversation history."""
        return self.thread.get_messages()
    
    def clear_thread(self):
        """Clear the conversation history."""
        self.thread.messages = []