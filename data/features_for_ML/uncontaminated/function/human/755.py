from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from telert.messaging import (
    MessagingConfig, 
    Provider, 
    configure_provider, 
    configure_providers,
    send_message
)

def set_default_provider(provider: Union[str, Provider]) -> None:
    """
    Set the default messaging provider.

    Args:
        provider: The provider to set as default

    Examples:
        from telert import set_default_provider

        set_default_provider("slack")
    """
    config = MessagingConfig()

    if isinstance(provider, str):
        provider = Provider.from_string(provider)

    config.set_default_provider(provider)