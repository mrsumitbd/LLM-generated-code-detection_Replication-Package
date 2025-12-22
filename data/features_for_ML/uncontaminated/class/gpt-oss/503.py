from __future__ import annotations

from typing import Dict, List, Optional, Type

class AdaptersRegistry:
    """
    Registry for all payment adapters.
    This class is used to register and retrieve adapters based on their provider.
    """

    _registry: Dict[str, Type["BaseAdapter"]] = {}

    @classmethod
    def register(cls, name: Optional[str] = None) -> None:  # type: ignore
        """
        Decorator to register an adapter class.

        Parameters
        ----------
        name : Optional[str]
            The key under which the adapter will be stored. If omitted,
            the class name is used.
        """
        def decorator(adapter_cls: Type["BaseAdapter"]) -> Type["BaseAdapter"]:
            reg_name = name or adapter_cls.__name__
            cls._registry[reg_name] = adapter_cls
            return adapter_cls

        return decorator

    @classmethod
    def get(cls, name: str) -> Type["BaseAdapter"]:  # type: ignore
        """
        Retrieve an adapter class by its registered name.

        Parameters
        ----------
        name : str
            The name of the adapter to retrieve.

        Returns
        -------
        Type[BaseAdapter]
            The adapter class associated with the given name.

        Raises
        ------
        KeyError
            If no adapter is registered under the given name.
        """
        try:
            return cls._registry[name]
        except KeyError as exc:
            raise KeyError(f"Adapter '{name}' not found in registry.") from exc

    @classmethod
    def all(cls) -> List[Type["BaseAdapter"]]:  # type: ignore
        """
        Return a list of all registered adapter classes.
        """
        return list(cls._registry.values())

    @classmethod
    def clear(cls) -> None:
        """
        Remove all adapters from the registry.
        """
        cls._registry.clear()

    @classmethod
    def list(cls) -> List[str]:
        """
        Return a list of all registered adapter names.
        """
        return list(cls._registry.keys())