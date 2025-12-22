from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import importlib
from typing import Any, Dict, Tuple, Type

# Registry for backend classes
_BACKEND_REGISTRY: Dict[str, Type[Any]] = {}
# Registry for singleton instances
_SINGLETON_INSTANCES: Dict[Tuple[Any, ...], Any] = {}


def register_backend(name: str):
    """
    Decorator to register a backend class under a given name.
    """
    def decorator(cls: Type[Any]) -> Type[Any]:
        _BACKEND_REGISTRY[name] = cls
        return cls
    return decorator


def _get_backend_class(name: str) -> Type[Any]:
    """
    Resolve a backend class by name.  First look in the registry, then try
    to import a module named ``{name}_backend`` and fetch a class named
    ``{Name}Backend``.
    """
    if name in _BACKEND_REGISTRY:
        return _BACKEND_REGISTRY[name]
    try:
        module = importlib.import_module(f"{name}_backend")
        class_name = f"{name.capitalize()}Backend"
        return getattr(module, class_name)
    except Exception as exc:
        raise ValueError(f"Could not find backend class for '{name}'.") from exc


def get_file_backend(
    uri: str | Path | None = None,
    *,
    backend_args: dict | None = None,
    enable_singleton: bool = False,
    backend_key: str | None = None,
):
    """
    Return a file backend based on the prefix of uri or backend_args.

    Args:
        uri (str or Path): Uri to be parsed that contains the file prefix.
        backend_args (dict, optional): Arguments to instantiate the
            corresponding backend. Defaults to None.
        enable_singleton (bool): Whether to enable the singleton pattern.
            If it is True, the backend created will be reused if the
            signature is same with the previous one. Defaults to False.
        backend_key: str: The key to register the backend. Defaults to None.

    Returns:
        BaseStorageBackend: Instantiated Backend object.
    """
    backend_args = backend_args or {}
    # Determine backend name
    if "backend" in backend_args:
        backend_name = backend_args.pop("backend")
    elif uri is not None:
        scheme = urlparse(str(uri)).scheme
        backend_name = scheme or "file"
    else:
        raise ValueError("Either `uri` or `backend_args['backend']` must be provided.")

    # Resolve backend class
    backend_cls = _get_backend_class(backend_name)

    # Build singleton key
    if enable_singleton:
        if backend_key is not None:
            key = (backend_key,)
        else:
            # Use backend name + sorted args as key
            args_tuple = tuple(sorted(backend_args.items()))
            key = (backend_name, args_tuple)
        if key in _SINGLETON_INSTANCES:
            return _SINGLETON_INSTANCES[key]

    # Instantiate backend
    backend = backend_cls(**backend_args)

    # Store singleton instance if requested
    if enable_singleton:
        _SINGLETON_INSTANCES[key] = backend

    return backend