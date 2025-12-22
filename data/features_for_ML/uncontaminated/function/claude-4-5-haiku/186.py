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
    if self._effective_config is not None:
        return self._effective_config
    
    import copy
    
    # Create a deep copy of the base configuration
    effective_config = copy.deepcopy(self._config)
    
    # Apply all overrides
    for key, value in self._overrides.items():
        effective_config[key] = value
    
    # Cache the result
    self._effective_config = effective_config
    
    return effective_config