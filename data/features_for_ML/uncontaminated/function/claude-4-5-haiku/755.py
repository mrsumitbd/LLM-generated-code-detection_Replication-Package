def set_default_provider(provider: Union[str, Provider]) -> None:
    """
    Set the default messaging provider.

    Args:
        provider: The provider to set as default

    Examples:
        from telert import set_default_provider

        set_default_provider("slack")
    """
    global _default_provider
    
    if isinstance(provider, str):
        provider_lower = provider.lower()
        if provider_lower not in _PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Available providers: {list(_PROVIDERS.keys())}")
        _default_provider = _PROVIDERS[provider_lower]
    elif isinstance(provider, Provider):
        _default_provider = provider
    else:
        raise TypeError(f"provider must be a string or Provider instance, got {type(provider)}")