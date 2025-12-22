class SlimConfig:
    """Configuration helper for SLIM applications."""

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        self._config = config_dict or {}

    @property
    def endpoint(self) -> str:
        return self._config.get('endpoint', 'localhost:50051')

    @property
    def tls_insecure(self) -> bool:
        return self._config.get('tls_insecure', True)

    def to_connection_config(self) -> Dict[str, Any]:
        return {
            'endpoint': self.endpoint,
            'tls_insecure': self.tls_insecure,
        }

    def to_server_config(self) -> Dict[str, Any]:
        return {
            'endpoint': self.endpoint,
            'tls_insecure': self.tls_insecure,
        }