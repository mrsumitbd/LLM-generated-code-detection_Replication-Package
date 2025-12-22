import json
from pathlib import Path

def get_file_backend(
    uri: str | Path | None = None,
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
    global backend_instances
    if backend_key is not None:
        if backend_key in backend_instances:
            return backend_instances[backend_key]

    if backend_args is None:
        backend_args = {}

    if uri is None and "backend" not in backend_args and backend_key is None:
        raise ValueError('uri should not be None when "backend" does not exist in backend_args and backend_key is None')

    if uri is not None:
        prefix = _parse_uri_prefix(uri)
    else:
        prefix = ""

    if enable_singleton:
        unique_key = f"{prefix}:{json.dumps(backend_args)}"
        if unique_key in backend_instances:
            return backend_instances[unique_key]

        backend = _get_file_backend(prefix, backend_args)
        backend_instances[unique_key] = backend
        if backend_key is not None:
            backend_instances[backend_key] = backend
        return backend
    else:
        backend = _get_file_backend(prefix, backend_args)
        return backend