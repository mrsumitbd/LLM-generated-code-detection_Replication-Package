from typing import Optional, Dict, Any

class ProviderRouter:
    """提供商路由器"""

    def __init__(self):
        self._provider_map = {
            "model1": {"provider": "provider1", "url": "https://example.com/provider1"},
            "model2": {"provider": "provider2", "url": "https://example.com/provider2"},
            "model3": {"provider": "provider3", "url": "https://example.com/provider3"}
        }

    def get_provider_for_model(self, model: str) -> Optional[Dict[str, str]]:
        if model in self._provider_map:
            return self._provider_map[model]
        return None

    def get_models_list(self) -> Dict[str, Any]:
        return self._provider_map