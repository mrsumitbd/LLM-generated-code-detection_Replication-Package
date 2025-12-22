from typing import Type

class RateLimiterRegistry:
    """Registry for RateLimiter classes."""
    _registry = {}

    @classmethod
    def get_register_key(cls, _type: str) -> str:
        return f"{cls.__name__}_{_type}"

    @classmethod
    def register(cls, new_cls):
        key = cls.get_register_key(new_cls._type)
        cls._registry[key] = new_cls

    @classmethod
    def get(cls, _type: str) -> Type["BaseRateLimiter"]:
        key = cls.get_register_key(_type)
        return cls._registry.get(key)