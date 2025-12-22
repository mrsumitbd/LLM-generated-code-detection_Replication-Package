def get_effective_config(self) -> dict[str, Any]:
    if getattr(self, '_effective_config', None) is None or self._overrides_changed:
        self._effective_config = self._get_effective_config()
        self._overrides_changed = False
    return self._effective_config

def _get_effective_config(self) -> dict[str, Any]:
    base_config = copy.deepcopy(self._base_config)
    for key, value in self._overrides.items():
        self._apply_override(base_config, key.split('.'), value)
    return base_config

def _apply_override(self, config: dict, keys: list[str], value: Any) -> None:
    current = config
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value