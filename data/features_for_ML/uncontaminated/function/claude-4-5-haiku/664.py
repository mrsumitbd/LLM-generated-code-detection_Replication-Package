def list_providers() -> List[Dict[str, Any]]:
    """
    List all configured providers.

    Returns:
        A list of dictionaries with provider information

    Examples:
        from telert import list_providers

        providers = list_providers()
        for p in providers:
            print(f"{p['name']} {'(default)' if p['is_default'] else ''}")
    """
    from telert.config import get_config
    
    config = get_config()
    providers = []
    
    if not config or 'providers' not in config:
        return providers
    
    default_provider = config.get('default_provider')
    
    for provider_name, provider_config in config.get('providers', {}).items():
        provider_info = {
            'name': provider_name,
            'type': provider_config.get('type'),
            'is_default': provider_name == default_provider,
            'config': {k: v for k, v in provider_config.items() if k != 'type'}
        }
        providers.append(provider_info)
    
    return providers