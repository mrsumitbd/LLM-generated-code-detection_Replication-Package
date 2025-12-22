from pathlib import Path

def get_file_backend(
    uri: str | Path | None = None,
    *,
    backend_args: dict | None = None,
    enable_singleton: bool = False,
    backend_key: str | None = None,
):
    if uri is not None:
        uri_prefix = uri.split(':')[0]
        if uri_prefix == 'http':
            return HttpStorageBackend(uri, enable_singleton, backend_key)
        elif uri_prefix == 'ftp':
            return FtpStorageBackend(uri, enable_singleton, backend_key)
        else:
            return FileStorageBackend(uri, enable_singleton, backend_key)
    elif backend_args is not None:
        if 'backend' in backend_args:
            backend_name = backend_args['backend']
            if backend_name == 'http':
                return HttpStorageBackend(uri, enable_singleton, backend_key)
            elif backend_name == 'ftp':
                return FtpStorageBackend(uri, enable_singleton, backend_key)
            else:
                return FileStorageBackend(uri, enable_singleton, backend_key)
        else:
            return FileStorageBackend(uri, enable_singleton, backend_key)
    else:
        return None