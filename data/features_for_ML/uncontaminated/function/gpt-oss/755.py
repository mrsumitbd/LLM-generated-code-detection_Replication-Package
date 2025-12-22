from typing import Union

# Assume Provider is defined elsewhere in the package
try:
    from .providers import Provider
except Exception:
    # Fallback: define a minimal Provider enum for type checking
    from enum import Enum
    class Provider(Enum):
        SLACK = "slack"
        EMAIL = "email"
        SMS = "sms"

# Global variable to hold the default provider
_default_provider: Provider | None = None

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

    # Resolve string to Provider enum
    if isinstance(provider, str):
        # Try to match by name (case-insensitive)
        try:
            provider = Provider[provider.upper()]
        except KeyError:
            # Try to match by value
            try:
                provider = Provider(provider.lower())
            except ValueError:
                raise ValueError(
                    f"Unknown provider '{provider}'. "
                    f"Valid providers are: {[p.value for p in Provider]}"
                ) from None

    if not isinstance(provider, Provider):
        raise TypeError(
            f"provider must be a str or Provider instance, got {type(provider).__name__}"
        )

    _default_provider = provider