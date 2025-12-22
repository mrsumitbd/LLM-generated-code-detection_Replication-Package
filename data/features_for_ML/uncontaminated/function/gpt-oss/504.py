import os
from typing import Type

# Try to import the real StorageBackend implementation if available.
try:
    from .storage_backend import StorageBackend
except Exception:
    # Fallback minimal implementation for environments where the real class is not available.
    class StorageBackend:
        """Minimal placeholder for StorageBackend."""
        def __init__(self, *args, **kwargs):
            pass

# Optional concrete backend implementations (simple placeholders).
class LocalStorageBackend(StorageBackend):
    """A simple local filesystem backend."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class S3StorageBackend(StorageBackend):
    """A simple S3 backend placeholder."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def get_storage_backend() -> StorageBackend:
    """
    Return an instance of the configured storage backend.

    The backend type is determined by the `STORAGE_BACKEND` environment variable.
    Supported values are:
        - 'local' (default): returns a LocalStorageBackend instance.
        - 's3': returns an S3StorageBackend instance.

    If the environment variable is not set or contains an unsupported value,
    the function falls back to the local backend.
    """
    backend_name = os.getenv("STORAGE_BACKEND", "local").lower()
    if backend_name == "s3":
        return S3StorageBackend()
    # Default to local backend for any other value.
    return LocalStorageBackend()