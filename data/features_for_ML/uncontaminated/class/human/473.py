from typing import Tuple, Optional, List, Dict, Any

class SlimConfig:
    """Configuration helper for SLIM applications."""

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        self.config = config_dict or {}

    @property
    def endpoint(self) -> str:
        return self.config.get("endpoint", "127.0.0.1:46357")

    @property
    def tls_insecure(self) -> bool:
        return self.config.get("tls", {}).get("insecure", True)

    def to_connection_config(self) -> Dict[str, Any]:
        """Convert to SLIM connection configuration."""
        return {
            "endpoint": f"http://{self.endpoint}"
            if not self.endpoint.startswith("http")
            else self.endpoint,
            "tls": {"insecure": self.tls_insecure},
        }

    def to_server_config(self) -> Dict[str, Any]:
        """Convert to SLIM server configuration."""
        return {"endpoint": self.endpoint, "tls": {"insecure": self.tls_insecure}}