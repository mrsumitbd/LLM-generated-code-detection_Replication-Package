import json
import os
from typing import Optional

import requests
from pydantic import BaseModel

from settings import Settings


class OllamaClient:
    """Client for interacting with Ollama local LLM service."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.session = requests.Session()

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate text using Ollama."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        
        if system:
            payload["system"] = system
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")

    def chat(self, messages: list[dict], system: Optional[str] = None) -> str:
        """Chat with Ollama using message history."""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        
        if system:
            payload["system"] = system
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if "message" in result:
            return result["message"].get("content", "")
        return ""

    def list_models(self) -> list[str]:
        """List available models."""
        url = f"{self.base_url}/api/tags"
        
        response = self.session.get(url)
        response.raise_for_status()
        
        result = response.json()
        models = result.get("models", [])
        return [model.get("name", "") for model in models]

    def pull_model(self, model_name: str) -> bool:
        """Pull a model from the registry."""
        url = f"{self.base_url}/api/pull"
        
        payload = {"name": model_name}
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        return response.status_code == 200

    def delete_model(self, model_name: str) -> bool:
        """Delete a model."""
        url = f"{self.base_url}/api/delete"
        
        payload = {"name": model_name}
        
        response = self.session.delete(url, json=payload)
        response.raise_for_status()
        
        return response.status_code == 200

    def show_model_info(self, model_name: str) -> dict:
        """Show information about a model."""
        url = f"{self.base_url}/api/show"
        
        payload = {"name": model_name}
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()