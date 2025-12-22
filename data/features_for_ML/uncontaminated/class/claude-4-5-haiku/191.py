import anthropic
import json
from typing import Optional, Dict, Any


class ProviderRouter:
    """提供商路由器"""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.models_cache = None

    def get_provider_for_model(self, model: str) -> Optional[Dict[str, str]]:
        """Get provider information for a specific model"""
        models_list = self.get_models_list()
        
        for provider, models in models_list.items():
            if isinstance(models, list):
                if model in models:
                    return {"provider": provider, "model": model}
            elif isinstance(models, dict):
                if model in models.get("models", []):
                    return {"provider": provider, "model": model}
        
        return None

    def get_models_list(self) -> Dict[str, Any]:
        """Get list of available models from Claude"""
        if self.models_cache is not None:
            return self.models_cache
        
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": """Please provide a JSON response listing AI model providers and their available models. 
                    Format the response as a JSON object where keys are provider names and values are lists of model names.
                    Include major providers like OpenAI, Anthropic, Google, etc.
                    Return ONLY valid JSON, no other text.
                    Example format:
                    {
                        "OpenAI": ["gpt-4", "gpt-3.5-turbo"],
                        "Anthropic": ["claude-3-opus", "claude-3-sonnet"],
                        "Google": ["gemini-pro", "gemini-pro-vision"]
                    }"""
                }
            ]
        )
        
        response_text = message.content[0].text
        
        try:
            models_dict = json.loads(response_text)
        except json.JSONDecodeError:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                models_dict = json.loads(json_str)
            else:
                models_dict = {
                    "OpenAI": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
                    "Anthropic": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
                    "Google": ["gemini-pro", "gemini-pro-vision"],
                    "Meta": ["llama-2-70b", "llama-2-13b"],
                    "Mistral": ["mistral-large", "mistral-medium", "mistral-small"]
                }
        
        self.models_cache = models_dict
        return models_dict