import os
from typing import Any, Dict

class ModelProviderConfig:
    def __init__(self, prefix: str, provider: str, base_url: str, env_var: str):
        self.prefix = prefix
        self.provider = provider
        self.base_url = base_url
        self.env_var = env_var

    def configure(self, model: str, kwargs: Dict[str, Any]) -> None:
        kwargs["model"] = model.replace(self.prefix, "")
        kwargs["custom_llm_provider"] = self.provider
        kwargs["base_url"] = self.base_url
        api_key = os.getenv(self.env_var)
        if not api_key:
            raise ValueError(f"{self.env_var} is not set in the environment variables.")
        kwargs["api_key"] = api_key