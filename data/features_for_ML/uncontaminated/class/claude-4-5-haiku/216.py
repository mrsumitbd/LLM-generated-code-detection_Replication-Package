import os
import json
import anthropic


class TaskRunner:
    """Ray remote class for executing distributed PPO training tasks.

    This class encapsulates the main training logic and runs as a Ray remote actor
    to enable distributed execution across multiple nodes and GPUs.
    """

    def run(self, config):
        """Execute a training task using Claude API with extended thinking.
        
        Args:
            config: Configuration dictionary containing task parameters
            
        Returns:
            Dictionary containing task results and metrics
        """
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        task_description = config.get("task_description", "")
        model = config.get("model", "claude-3-7-sonnet-20250219")
        max_tokens = config.get("max_tokens", 16000)
        budget_tokens = config.get("budget_tokens", 10000)
        
        messages = [
            {
                "role": "user",
                "content": task_description
            }
        ]
        
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            thinking={
                "type": "enabled",
                "budget_tokens": budget_tokens
            },
            messages=messages
        )
        
        result = {
            "status": "completed",
            "model": model,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            "content": []
        }
        
        for block in response.content:
            if block.type == "thinking":
                result["content"].append({
                    "type": "thinking",
                    "text": block.thinking
                })
            elif block.type == "text":
                result["content"].append({
                    "type": "text",
                    "text": block.text
                })
        
        return result