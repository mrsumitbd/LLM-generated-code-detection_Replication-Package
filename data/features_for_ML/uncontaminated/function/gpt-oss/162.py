import threading
from typing import Optional

# Assume MemoryBackend is defined elsewhere in the same package
try:
    from .backend import MemoryBackend  # type: ignore
except Exception:
    # Fallback for environments where the relative import fails
    from backend import MemoryBackend  # type: ignore

# Module‑level cache for the singleton instance
_backend_instance: Optional[MemoryBackend] = None
_backend_lock = threading.Lock()


def _get_backend() -> MemoryBackend:
    """
    Return a singleton instance of MemoryBackend. The instance is lazily
    created on first call and cached for subsequent calls. Thread‑safe.
    """
    global _backend_instance
    if _backend_instance is None:
        with _backend_lock:
            if _backend_instance is None:
                _backend_instance = MemoryBackend()
    return _backend_instance