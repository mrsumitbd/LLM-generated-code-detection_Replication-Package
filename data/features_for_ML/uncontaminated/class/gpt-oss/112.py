from __future__ import annotations

from datetime import timedelta
from typing import Protocol, Iterable, List, Optional


class ObjectStore(Protocol):
    """Protocol for an underlying object storage backend."""

    def put_object(
        self,
        key: str,
        data: bytes,
        *,
        content_type: Optional[str] = None,
    ) -> None:
        """Store an object identified by *key* with the given *data*."""
        ...

    def get_object(self, key: str) -> bytes:
        """Retrieve the object identified by *key*."""
        ...

    def delete_object(self, key: str) -> None:
        """Delete the object identified by *key*."""
        ...

    def list_objects(self, prefix: str = "") -> List[str]:
        """Return a list of object keys that start with *prefix*."""
        ...

    def generate_presigned_url(
        self, key: str, expiration: timedelta
    ) -> str:
        """Return a presigned URL for the object identified by *key*."""
        ...


class ResourceStore:
    """
    A thin wrapper around an :class:`ObjectStore` that provides convenient
    methods for common resource operations and presigned URL generation.
    """

    def __init__(
        self,
        *,
        store: ObjectStore,
        presigned_url_expiration: timedelta = timedelta(days=7),
    ) -> None:
        self._store = store
        self._presigned_url_expiration = presigned_url_expiration

    # ------------------------------------------------------------------
    # Basic CRUD operations
    # ------------------------------------------------------------------
    def upload(
        self,
        key: str,
        data: bytes,
        *,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Store *data* under *key* in the underlying object store.

        Returns the key that was used for storage.
        """
        self._store.put_object(key, data, content_type=content_type)
        return key

    def download(self, key: str) -> bytes:
        """
        Retrieve the data stored under *key*.
        """
        return self._store.get_object(key)

    def delete(self, key: str) -> None:
        """
        Delete the object identified by *key*.
        """
        self._store.delete_object(key)

    def list(self, prefix: str = "") -> List[str]:
        """
        List all object keys that start with *prefix*.
        """
        return self._store.list_objects(prefix=prefix)

    # ------------------------------------------------------------------
    # Presigned URL handling
    # ------------------------------------------------------------------
    def generate_presigned_url(
        self,
        key: str,
        *,
        expiration: Optional[timedelta] = None,
    ) -> str:
        """
        Generate a presigned URL for the object identified by *key*.

        If *expiration* is not provided, the default expiration set during
        construction is used.
        """
        exp = expiration or self._presigned_url_expiration
        return self._store.generate_presigned_url(key, expiration=exp)

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    def exists(self, key: str) -> bool:
        """
        Return ``True`` if an object with *key* exists in the store.
        """
        try:
            self._store.get_object(key)
            return True
        except Exception:
            return False

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(store={self._store!r}, "
            f"presigned_url_expiration={self._presigned_url_expiration!r})"
        )