import os
import openai

class OpenAIClient:
    """Call OpenAI's Chat Completions API."""

    def __init__(self, api_key: str = None):
        if api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY")
        else:
            self.api_key = api_key
        openai.api_key = self.api_key

    def complete(self, prompt: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()