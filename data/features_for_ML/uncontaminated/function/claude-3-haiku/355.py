from pathlib import Path
from typing import Union

from .base import BaseStorageBackend
from .registry import BACKENDS, get_backend

def get_file_backend(
    uri: Union[str, Path, None] = None,
    *,
    backend_args: dict | None = None,
    enable_singleton: bool = False,
    backend_key: str | None = None,
):
    """Return a file backend based on the prefix of uri or backend_args.

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

    Examples:
        >>> # get file backend based on the prefix of uri
        >>> uri = 'http://path/of/your/file'
        >>> backend = get_file_backend(uri)
        >>> # get file backend based on the backend_args
        >>> backend = get_file_backend(backend_args={'backend': 'http'})
        >>> # backend name has a higher priority if 'backend' in backend_args
        >>> backend = get_file_backend(uri, backend_args={'backend': 'http'})
    """
    if backend_args is None:
        backend_args = {}

    if uri is not None:
        uri = str(uri)
        for prefix, backend_cls in BACKENDS.items():
            if uri.startswith(prefix):
                backend_args['uri'] = uri
                return get_backend(
                    backend_cls,
                    backend_args=backend_args,
                    enable_singleton=enable_singleton,
                    backend_key=backend_key,
                )

    if 'backend' in backend_args:
        backend_cls = BACKENDS.get(backend_args['backend'])
        if backend_cls is not None:
            return get_backend(
                backend_cls,
                backend_args=backend_args,
                enable_singleton=enable_singleton,
                backend_key=backend_key,
            )

    raise ValueError(f'No backend found for uri={uri} or backend_args={backend_args}')