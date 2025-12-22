from typing import Dict, Any

class ModelProviderConfig:

    def __init__(self, prefix: str, provider: str, base_url: str, env_var: str):
        self.prefix = prefix
        self.provider = provider
        self.base_url = base_url
        self.env_var = env_var

    def configure(self, model: str, kwargs: Dict[str, Any]) -> None:
        print(f"Configuring model '{model}' with kwargs: {kwargs}")

# Example Usage
config = ModelProviderConfig("model_", "provider1", "http://example.com", "MODEL_ENV")
config.configure("model1", {"param1": 123, "param2": "abc"})