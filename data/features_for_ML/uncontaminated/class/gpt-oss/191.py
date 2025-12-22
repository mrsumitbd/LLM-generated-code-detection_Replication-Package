from typing import Any, Dict, Optional

class ProviderRouter:
    """提供商路由器"""

    def __init__(self):
        # 内部映射：模型名称 -> 提供商信息
        self._model_provider_map: Dict[str, Dict[str, str]] = {
            "gpt-3.5-turbo": {"provider": "OpenAI", "api_key": "YOUR_OPENAI_KEY"},
            "gpt-4": {"provider": "OpenAI", "api_key": "YOUR_OPENAI_KEY"},
            "claude-2": {"provider": "Anthropic", "api_key": "YOUR_ANTHROPIC_KEY"},
            "gemini-pro": {"provider": "Google", "api_key": "YOUR_GOOGLE_KEY"},
        }

    def get_provider_for_model(self, model: str) -> Optional[Dict[str, str]]:
        """
        根据模型名称返回对应的提供商信息。

        :param model: 模型名称
        :return: 提供商信息字典，若不存在则返回 None
        """
        return self._model_provider_map.get(model)

    def get_models_list(self) -> Dict[str, Any]:
        """
        返回所有已配置模型及其对应的提供商信息。

        :return: 模型名称到提供商信息的映射
        """
        return dict(self._model_provider_map)