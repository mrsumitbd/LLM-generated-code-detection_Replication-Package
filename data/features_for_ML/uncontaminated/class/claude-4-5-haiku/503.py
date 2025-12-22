class AdaptersRegistry:
    """
    Registry for all payment adapters.
    This class is used to register and retrieve adapters based on their provider.
    """
    
    _registry: dict[str, Type["BaseAdapter"]] = {}

    @classmethod
    def register(cls, name: Optional[str] = None) -> None:  # type: ignore
        def decorator(adapter_class: Type["BaseAdapter"]) -> Type["BaseAdapter"]:
            adapter_name = name or adapter_class.__name__
            cls._registry[adapter_name] = adapter_class
            return adapter_class
        return decorator

    @classmethod
    def get(cls, name: str) -> Type["BaseAdapter"]:  # type: ignore
        if name not in cls._registry:
            raise KeyError(f"Adapter '{name}' not found in registry")
        return cls._registry[name]

    @classmethod
    def all(cls) -> List[Type["BaseAdapter"]]:  # type: ignore
        return list(cls._registry.values())

    @classmethod
    def clear(cls) -> None:
        cls._registry.clear()

    @classmethod
    def list(cls) -> List[str]:
        return list(cls._registry.keys())