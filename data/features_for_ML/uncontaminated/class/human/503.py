from easyswitch.exceptions import InvalidProviderError
from typing import Any, ClassVar, Dict, List, Optional, Type

class AdaptersRegistry:
    """
    Registry for all payment adapters.
    This class is used to register and retrieve adapters based on their provider.
    """
    
    _registry: ClassVar[Dict[str, Type["BaseAdapter"]]] = {} # type: ignore

    @classmethod
    def register(cls, name: Optional[str] = None) -> None: # type: ignore
        """Register a new Adapter class."""

        def wrapper(adapter: Type["BaseAdapter"]):
            """Wrapper"""

            nonlocal name
            name = name or adapter.provider_name()
            name = name.upper()
            if name not in cls._registry.keys():
                cls._registry[name] = adapter
                
            return adapter

        return wrapper

    @classmethod
    def get(cls, name: str) -> Type["BaseAdapter"]: # type: ignore
        """Get an Adapter class by its name."""

        if name not in cls._registry:
            raise InvalidProviderError(
                f"Invalid Adapter name: '{name}' not found."
                )
        
        return cls._registry[name]

    @classmethod
    def all(cls) -> List[Type["BaseAdapter"]]: # type: ignore
        """Get all registered Adapters classes."""
        return list(cls._registry.values())

    @classmethod
    def clear(cls) -> None:
        """Clear the registry."""
        cls._registry.clear()

    @classmethod
    def list(cls) -> List[str]:
        """List all registered Adapters names."""
        return list(cls._registry.keys())