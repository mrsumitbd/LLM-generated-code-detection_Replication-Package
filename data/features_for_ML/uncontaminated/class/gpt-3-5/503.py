from typing import Optional, Type, List

class AdaptersRegistry:
    adapters = {}

    @classmethod
    def register(cls, name: Optional[str] = None) -> None:
        def decorator(adapter_cls):
            cls.adapters[name] = adapter_cls
            return adapter_cls
        return decorator

    @classmethod
    def get(cls, name: str) -> Type["BaseAdapter"]:
        return cls.adapters.get(name)

    @classmethod
    def all(cls) -> List[Type["BaseAdapter"]]:
        return list(cls.adapters.values())

    @classmethod
    def clear(cls) -> None:
        cls.adapters = {}

    @classmethod
    def list(cls) -> List[str]:
        return list(cls.adapters.keys())