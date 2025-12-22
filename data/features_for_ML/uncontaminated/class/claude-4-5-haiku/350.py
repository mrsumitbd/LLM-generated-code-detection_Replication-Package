import os
from anthropic import Anthropic

class OpenAIClient:
    """Call OpenAI's Chat Completions API."""

    def __init__(self):
        self.client = Anthropic()
        self.conversation_history = []

    def complete(self, prompt: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8096,
            system="You are a helpful assistant.",
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message