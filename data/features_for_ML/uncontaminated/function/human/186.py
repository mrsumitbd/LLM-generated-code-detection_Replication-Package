from typing import Any
from copy import deepcopy

def get_effective_config(self) -> dict[str, Any]:
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
        # Return cached config if available
        if self._effective_config is not None:
            return self._effective_config

        # Create deep copy to avoid modifying base config
        config = deepcopy(self.base_config)

        # Apply each override to the config copy
        for path, value in self.overrides.items():
            self._update_config_value(config, path, value)

        # Return the result
        self._effective_config = config
        return config