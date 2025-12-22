from typing import Dict, List, Optional, Set, Tuple, Type
from ..exceptions import SetUpError
from ..types import AtomicActionP, AtomicActionTypeT, RateLimiterTypeT, StoreP

class RateLimiterRegistry:
    """Registry for RateLimiter classes."""

    # The namespace for the RateLimiter classes.
    _NAMESPACE: str = "sync"

    # A dictionary to hold the registered RateLimiter classes.
    _RATE_LIMITERS: Dict[RateLimiterTypeT, Type["BaseRateLimiter"]] = {}

    @classmethod
    def get_register_key(cls, _type: str) -> str:
        """Get the register key for the RateLimiter classes."""
        return f"{cls._NAMESPACE}:{_type}"

    @classmethod
    def register(cls, new_cls):
        try:
            cls._RATE_LIMITERS[cls.get_register_key(new_cls.Meta.type)] = new_cls
        except AttributeError as e:
            raise SetUpError("failed to register RateLimiter: {}".format(e))

    @classmethod
    def get(cls, _type: RateLimiterTypeT) -> Type["BaseRateLimiter"]:
        try:
            return cls._RATE_LIMITERS[cls.get_register_key(_type)]
        except KeyError:
            raise SetUpError("{} not found".format(_type))