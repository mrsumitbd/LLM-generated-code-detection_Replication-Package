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
    from pathlib import Path
    
    if backend_args is None:
        backend_args = {}
    else:
        backend_args = backend_args.copy()
    
    # Determine backend name
    backend_name = backend_args.pop('backend', None)
    
    if backend_name is None:
        if uri is None:
            raise ValueError('uri and backend_args cannot both be None or empty')
        
        uri_str = str(uri)
        
        # Extract prefix from uri
        if '://' in uri_str:
            backend_name = uri_str.split('://')[0]
        else:
            backend_name = 'disk'
    
    # Import registry and get backend class
    from mmengine.registry import Registry
    from mmengine.fileio.backends import (
        LocalBackend,
        HTTPBackend,
        PetrelBackend,
        MemoryBackend,
        LmdbBackend,
    )
    
    # Map backend names to classes
    backend_map = {
        'disk': LocalBackend,
        'local': LocalBackend,
        'http': HTTPBackend,
        'https': HTTPBackend,
        'petrel': PetrelBackend,
        's3': PetrelBackend,
        'memory': MemoryBackend,
        'lmdb': LmdbBackend,
    }
    
    if backend_name not in backend_map:
        raise ValueError(f'Unsupported backend: {backend_name}')
    
    backend_class = backend_map[backend_name]
    
    # Create signature for singleton pattern
    if enable_singleton:
        import hashlib
        import json
        
        sig_dict = {'backend': backend_name, 'args': backend_args}
        sig_str = json.dumps(sig_dict, sort_keys=True, default=str)
        signature = hashlib.md5(sig_str.encode()).hexdigest()
        
        if not hasattr(get_file_backend, '_backend_cache'):
            get_file_backend._backend_cache = {}
        
        cache_key = backend_key or signature
        
        if cache_key in get_file_backend._backend_cache:
            return get_file_backend._backend_cache[cache_key]
        
        backend = backend_class(**backend_args)
        get_file_backend._backend_cache[cache_key] = backend
        return backend
    else:
        return backend_class(**backend_args)