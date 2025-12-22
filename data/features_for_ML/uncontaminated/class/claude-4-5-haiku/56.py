class RateLimiterRegistry:
    """Registry for RateLimiter classes."""

    _registry: dict[str, Type["BaseRateLimiter"]] = {}

    @classmethod
    def get_register_key(cls, _type: str) -> str:
        return _type.lower()

    @classmethod
    def register(cls, new_cls):
        key = cls.get_register_key(new_cls.__name__)
        cls._registry[key] = new_cls
        return new_cls

    @classmethod
    def get(cls, _type: RateLimiterTypeT) -> Type["BaseRateLimiter"]:
        key = cls.get_register_key(_type)
        if key not in cls._registry:
            raise ValueError(f"RateLimiter type '{_type}' not found in registry")
        return cls._registry[key]