from __future__ import annotations

from typing import Dict, Type, Any

# Assume these are defined elsewhere in the project
# from .base import BaseRateLimiter
# from .types import RateLimiterTypeT

# For the purpose of this implementation we provide minimal stubs.
# In real usage, replace these with the actual imports.
class BaseRateLimiter:
    """Base class for all rate limiters."""
    pass

RateLimiterTypeT = str  # Alias for the type identifier used by rate limiters


class RateLimiterRegistry:
    """Registry for RateLimiter classes."""

    # Internal registry mapping a unique key to a rate‑limiter class
    _registry: Dict[str, Type[BaseRateLimiter]] = {}

    @classmethod
    def get_register_key(cls, _type: str) -> str:
        """
        Return a unique key for the registry based on the provided type string.
        """
        return f"rate_limiter:{_type}"

    @classmethod
    def register(cls, new_cls: Type[BaseRateLimiter]) -> None:
        """
        Register a new rate‑limiter class.

        The class must expose a ``type`` attribute that identifies it.
        """
        if not hasattr(new_cls, "type"):
            raise AttributeError(
                f"Cannot register {new_cls!r}: missing required 'type' attribute"
            )
        key = cls.get_register_key(new_cls.type)
        if key in cls._registry:
            raise KeyError(f"RateLimiter type '{new_cls.type}' is already registered")
        cls._registry[key] = new_cls

    @classmethod
    def get(cls, _type: RateLimiterTypeT) -> Type[BaseRateLimiter]:
        """
        Retrieve a registered rate‑limiter class by its type identifier.

        Raises:
            KeyError: If no class is registered for the given type.
        """
        key = cls.get_register_key(_type)
        try:
            return cls._registry[key]
        except KeyError as exc:
            raise KeyError(f"No RateLimiter registered for type '{_type}'") from exc