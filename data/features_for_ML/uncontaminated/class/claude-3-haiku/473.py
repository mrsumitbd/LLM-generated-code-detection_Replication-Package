from typing import Dict, Any, Optional

class SlimConfig:
    """Configuration helper for SLIM applications."""

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        self._config_dict = config_dict or {}

    @property
    def endpoint(self) -> str:
        return self._config_dict.get('endpoint', '')

    @property
    def tls_insecure(self) -> bool:
        return self._config_dict.get('tls_insecure', False)

    def to_connection_config(self) -> Dict[str, Any]:
        return {
            'endpoint': self.endpoint,
            'tls_insecure': self.tls_insecure
        }

    def to_server_config(self) -> Dict[str, Any]:
        return self._config_dict