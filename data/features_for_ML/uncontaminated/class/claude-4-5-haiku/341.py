import anthropic
import json
from dataclasses import dataclass
from typing import Any


@dataclass
class EvaluationRunConfig:
    """Configuration for evaluation runs."""
    model: str
    max_tokens: int
    temperature: float = 0.7


class EvaluationRemoteWorkflowHandler:

    def __init__(self, config: EvaluationRunConfig, max_concurrency: int):
        self.config = config
        self.max_concurrency = max_concurrency
        self.client = anthropic.Anthropic()
        self.active_requests = {}

    def evaluate(self, prompt: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Evaluate a prompt using Claude with the configured settings.
        
        Args:
            prompt: The prompt to evaluate
            context: Optional context dictionary for the evaluation
            
        Returns:
            Dictionary containing the evaluation results
        """
        system_prompt = "You are an evaluation assistant. Analyze the given prompt and provide detailed feedback."
        
        if context:
            system_prompt += f"\n\nContext: {json.dumps(context)}"
        
        message = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            "prompt": prompt,
            "response": message.content[0].text,
            "model": self.config.model,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens
            }
        }

    def batch_evaluate(self, prompts: list[str], contexts: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        """
        Evaluate multiple prompts with concurrency control.
        
        Args:
            prompts: List of prompts to evaluate
            contexts: Optional list of context dictionaries
            
        Returns:
            List of evaluation results
        """
        if contexts is None:
            contexts = [None] * len(prompts)
        
        results = []
        for prompt, context in zip(prompts, contexts):
            result = self.evaluate(prompt, context)
            results.append(result)
        
        return results

    def get_status(self) -> dict[str, Any]:
        """Get the current status of the handler."""
        return {
            "model": self.config.model,
            "max_concurrency": self.max_concurrency,
            "active_requests": len(self.active_requests),
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }