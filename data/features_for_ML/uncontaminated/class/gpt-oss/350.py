import os
import openai
from typing import Optional


class OpenAIClient:
    """Call OpenAI's Chat Completions API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 150,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided via argument or OPENAI_API_KEY env var")
        openai.api_key = self.api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def complete(self, prompt: str) -> str:
        """
        Send a prompt to the OpenAI chat completion endpoint and return the assistant's reply.

        Parameters
        ----------
        prompt : str
            The user prompt to send to the model.

        Returns
        -------
        str
            The assistant's reply text. Returns an empty string if an error occurs.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                n=1,
                stop=None,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return ""