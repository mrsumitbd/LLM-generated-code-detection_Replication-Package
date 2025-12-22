from typing import Union

class StorageBackend:
    def __init__(self, name: str):
        self.name = name

def get_storage_backend() -> StorageBackend:
    return StorageBackend("LocalFileSystem")