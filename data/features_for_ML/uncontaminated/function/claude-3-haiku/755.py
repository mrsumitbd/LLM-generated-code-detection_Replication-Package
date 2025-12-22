from typing import Union
from .providers import Provider

def set_default_provider(provider: Union[str, Provider]) -> None:
    """
    Set the default messaging provider.

    Args:
        provider: The provider to set as default

    Examples:
        from telert import set_default_provider

        set_default_provider("slack")
    """
    from .config import set_default_provider as set_provider
    set_provider(provider)