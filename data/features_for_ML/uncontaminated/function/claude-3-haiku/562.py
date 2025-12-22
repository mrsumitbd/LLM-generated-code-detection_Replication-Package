import os
from typing import Type

from .base import BaseStateBackend
from .file import FileStateBackend
from .memory import MemoryStateBackend
from .redis import RedisStateBackend

def _get_default_backend() -> BaseStateBackend:
    """Get or create the default backend instance.

    Returns:
        The default backend instance.
    """
    backend_type = os.getenv("STATE_BACKEND", "memory")
    backend_classes: dict[str, Type[BaseStateBackend]] = {
        "file": FileStateBackend,
        "memory": MemoryStateBackend,
        "redis": RedisStateBackend,
    }
    backend_class = backend_classes.get(backend_type, MemoryStateBackend)
    return backend_class()