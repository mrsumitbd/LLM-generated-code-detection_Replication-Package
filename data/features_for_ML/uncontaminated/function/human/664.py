from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from telert.messaging import (
    MessagingConfig, 
    Provider, 
    configure_provider, 
    configure_providers,
    send_message
)

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
    config = MessagingConfig()
    default = config.get_default_provider()
    result = []

    for p in Provider:
        if config.is_provider_configured(p):
            provider_config = config.get_provider_config(p)
            info = {
                "name": p.value,
                "is_default": (default == p),
                "config": provider_config,
            }
            result.append(info)

    return result