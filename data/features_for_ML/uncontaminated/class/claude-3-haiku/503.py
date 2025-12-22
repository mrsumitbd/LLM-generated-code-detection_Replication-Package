from typing import Optional, Type, List
from .base_adapter import BaseAdapter

class AdaptersRegistry:
    """
    Registry for all payment adapters.
    This class is used to register and retrieve adapters based on their provider.
    """

    _registry: dict[str, Type[BaseAdapter]] = {}

    @classmethod
    def register(cls, name: Optional[str] = None) -> None:
        def wrapper(adapter: Type[BaseAdapter]) -> Type[BaseAdapter]:
            cls._registry[name or adapter.__name__] = adapter
            return adapter
        return wrapper

    @classmethod
    def get(cls, name: str) -> Type[BaseAdapter]:
        try:
            return cls._registry[name]
        except KeyError:
            raise ValueError(f"Adapter '{name}' not found in the registry.")

    @classmethod
    def all(cls) -> List[Type[BaseAdapter]]:
        return list(cls._registry.values())

    @classmethod
    def clear(cls) -> None:
        cls._registry.clear()

    @classmethod
    def list(cls) -> List[str]:
        return list(cls._registry.keys())