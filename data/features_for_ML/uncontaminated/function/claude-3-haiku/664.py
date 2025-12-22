from typing import List, Dict, Any
import telert.config as config

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
    providers = []
    for provider_name, provider_config in config.PROVIDERS.items():
        provider = {
            "name": provider_name,
            "is_default": provider_config.get("is_default", False),
            "config": provider_config
        }
        providers.append(provider)
    return providers