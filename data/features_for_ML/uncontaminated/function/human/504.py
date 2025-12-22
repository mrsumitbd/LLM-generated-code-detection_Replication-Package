import os

def get_storage_backend() -> StorageBackend:
    backend = os.environ.get("STORAGE_BACKEND", "local")
    if backend in ["s3", "minio"]:
        return S3Storage()
    else:
        return LocalStorage()