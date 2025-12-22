from typing import Optional, Dict, Any

class ProviderRouter:
    """提供商路由器"""

    def __init__(self):
        self.providers = {}

    def get_provider_for_model(self, model: str) -> Optional[Dict[str, str]]:
        return self.providers.get(model)

    def get_models_list(self) -> Dict[str, Any]:
        return self.providers

# Usage example:
# router = ProviderRouter()
# router.providers = {
#     'model1': {'provider': 'provider1'},
#     'model2': {'provider': 'provider2'}
# }
# print(router.get_provider_for_model('model1'))
# print(router.get_models_list())