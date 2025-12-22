import os
import httpx
from typing import Optional, Protocol

class OpenAIClient:
    """Call OpenAI's Chat Completions API."""

    model: str = "gpt-4o-mini"
    api_key: Optional[str] = None
    base_url: str = "https://api.openai.com/v1"

    def complete(self, prompt: str) -> str:
        key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY not set")
        headers = {"Authorization": f"Bearer {key}"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        resp = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()