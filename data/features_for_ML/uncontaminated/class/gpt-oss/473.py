from typing import Any, Dict, Optional


class SlimConfig:
    """Configuration helper for SLIM applications."""

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration helper.

        Parameters
        ----------
        config_dict : Optional[Dict[str, Any]]
            A dictionary containing configuration values. If None, an empty
            configuration is used.
        """
        self._config: Dict[str, Any] = config_dict or {}

    @property
    def endpoint(self) -> str:
        """
        Return the configured endpoint.

        Returns
        -------
        str
            The endpoint URL. Defaults to 'http://localhost' if not set.
        """
        return self._config.get("endpoint", "http://localhost")

    @property
    def tls_insecure(self) -> bool:
        """
        Return whether TLS verification is disabled.

        Returns
        -------
        bool
            True if TLS verification should be skipped, False otherwise.
        """
        return bool(self._config.get("tls_insecure", False))

    def to_connection_config(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary suitable for a client
        connection.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing at least the endpoint and TLS flag.
        """
        return {
            "endpoint": self.endpoint,
            "tls_insecure": self.tls_insecure,
        }

    def to_server_config(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary suitable for a server
        configuration.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing all configuration values except those
            used for the client connection (endpoint and tls_insecure).
        """
        return {
            k: v
            for k, v in self._config.items()
            if k not in ("endpoint", "tls_insecure")
        }