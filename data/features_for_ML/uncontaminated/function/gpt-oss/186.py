from copy import deepcopy
from typing import Any, Dict

class ConfigManager:
    def __init__(self, base_config: Dict[str, Any]):
        self._base_config: Dict[str, Any] = base_config
        self._overrides: Dict[str, Any] = {}
        self._effective_config: Dict[str, Any] | None = None
        self._config_dirty: bool = True

    def set_override(self, key: str, value: Any) -> None:
        """Set an override for a configuration key."""
        self._overrides[key] = value
        self._config_dirty = True

    def get_effective_config(self) -> Dict[str, Any]:
        """Get the configuration with all overrides applied.

        Creates a new configuration dictionary by applying all stored overrides
        to a deep copy of the base configuration. Caches the result to avoid
        recomputing unless overrides change.

        Returns:
            Dict containing the full configuration with all overrides applied

        Note:
            The configuration is cached in self._effective_config and only
            recomputed when new overrides are added via set_override()
        """
        if self._effective_config is None or self._config_dirty:
            # Start with a deep copy of the base configuration
            effective = deepcopy(self._base_config)

            # Apply each override
            for key, value in self._overrides.items():
                # Support nested keys using dot notation
                parts = key.split(".")
                d = effective
                for part in parts[:-1]:
                    if part not in d or not isinstance(d[part], dict):
                        d[part] = {}
                    d = d[part]
                d[parts[-1]] = value

            # Cache the result
            self._effective_config = effective
            self._config_dirty = False

        return deepcopy(self._effective_config)