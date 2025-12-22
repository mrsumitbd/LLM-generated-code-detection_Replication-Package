import requests
from typing import Dict, Any

class OllamaClient:
    """Client for interacting with Ollama local LLM service."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = f"{settings.host}:{settings.port}"
        self.headers = {"Content-Type": "application/json"}

    def generate_text(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7, top_p: float = 0.9, num_completions: int = 1) -> Dict[str, Any]:
        """Generate text using the Ollama LLM service."""
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "num_completions": num_completions
        }
        response = requests.post(f"{self.base_url}/generate", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_model_info(self) -> Dict[str, Any]:
        """Retrieve information about the Ollama LLM model."""
        response = requests.get(f"{self.base_url}/model_info", headers=self.headers)
        response.raise_for_status()
        return response.json()