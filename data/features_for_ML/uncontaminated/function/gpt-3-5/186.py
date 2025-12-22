def get_effective_config(self) -> dict[str, Any]:
    if not hasattr(self, '_effective_config'):
        self._effective_config = copy.deepcopy(self._base_config)
        for key, value in self._overrides.items():
            self._apply_override(self._effective_config, key, value)
    return self._effective_config