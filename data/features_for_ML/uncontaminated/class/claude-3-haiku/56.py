from typing import Type, TypeVar

RateLimiterTypeT = TypeVar("RateLimiterTypeT", bound=str)

class BaseRateLimiter:
    pass

class RateLimiterRegistry:
    """Registry for RateLimiter classes."""
    _registry = {}

    @classmethod
    def get_register_key(cls, _type: str) -> str:
        return _type.lower()

    @classmethod
    def register(cls, new_cls):
        register_key = cls.get_register_key(new_cls.__name__)
        cls._registry[register_key] = new_cls

    @classmethod
    def get(cls, _type: RateLimiterTypeT) -> Type["BaseRateLimiter"]:
        register_key = cls.get_register_key(_type)
        return cls._registry[register_key]