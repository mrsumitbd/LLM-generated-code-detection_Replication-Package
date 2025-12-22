from __future__ import annotations

from typing import Optional

# Assume BaseStateBackend is defined elsewhere and imported here
# from .backend import BaseStateBackend

# Global variable to hold the default backend instance
_default_backend: Optional[BaseStateBackend] = None


def _get_default_backend() -> BaseStateBackend:
    """Get or create the default backend instance.

    Returns:
        The default backend instance.
    """
    global _default_backend
    if _default_backend is None:
        # Create a new instance of the default backend.
        # If a specific default backend class is required, replace
        # BaseStateBackend() with that class.
        _default_backend = BaseStateBackend()
    return _default_backend