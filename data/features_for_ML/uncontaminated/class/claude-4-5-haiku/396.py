import anthropic
import json
import time
from datetime import datetime


class WatchDog:

    def __init__(self, **kwargs):
        self.client = anthropic.Anthropic()
        self.model = kwargs.get("model", "claude-3-5-sonnet-20241022")
        self.system_prompt = kwargs.get(
            "system_prompt",
            "You are a helpful assistant that monitors and analyzes system metrics and logs."
        )
        self.max_tokens = kwargs.get("max_tokens", 1024)
        self.conversation_history = []

    def analyze(self, query: str) -> str:
        """Analyze a query using Claude with multi-turn conversation support."""
        self.conversation_history.append({
            "role": "user",
            "content": query
        })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def monitor(self, metrics: dict) -> dict:
        """Monitor system metrics and provide analysis."""
        metrics_str = json.dumps(metrics, indent=2)
        query = f"Please analyze these system metrics and identify any issues:\n{metrics_str}"

        analysis = self.analyze(query)

        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "analysis": analysis
        }

    def check_logs(self, logs: list) -> str:
        """Check and analyze logs for issues."""
        logs_str = "\n".join(logs)
        query = f"Please review these logs and identify any errors or warnings:\n{logs_str}"

        return self.analyze(query)

    def get_recommendations(self) -> str:
        """Get recommendations based on previous analysis."""
        query = "Based on our previous conversation, what are your top recommendations for system improvement?"

        return self.analyze(query)

    def reset_conversation(self) -> None:
        """Reset the conversation history."""
        self.conversation_history = []

    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt."""
        self.system_prompt = prompt

    def get_conversation_history(self) -> list:
        """Get the current conversation history."""
        return self.conversation_history.copy()