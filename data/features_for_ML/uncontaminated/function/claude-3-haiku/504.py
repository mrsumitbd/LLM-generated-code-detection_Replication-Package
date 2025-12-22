from typing import Union
from abc import ABC, abstractmethod

class StorageBackend(ABC):
    @abstractmethod
    def store(self, data: bytes) -> str:
        pass

    @abstractmethod
    def retrieve(self, key: str) -> bytes:
        pass

class LocalFileSystemBackend(StorageBackend):
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def store(self, data: bytes) -> str:
        import os
        import uuid

        key = str(uuid.uuid4())
        file_path = os.path.join(self.base_dir, key)
        with open(file_path, 'wb') as file:
            file.write(data)
        return key

    def retrieve(self, key: str) -> bytes:
        import os
        file_path = os.path.join(self.base_dir, key)
        with open(file_path, 'rb') as file:
            return file.read()

class S3Backend(StorageBackend):
    def __init__(self, bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        import boto3
        self.s3 = boto3.resource('s3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
        self.bucket = self.s3.Bucket(bucket_name)

    def store(self, data: bytes) -> str:
        import uuid
        key = str(uuid.uuid4())
        self.bucket.put_object(Key=key, Body=data)
        return key

    def retrieve(self, key: str) -> bytes:
        obj = self.bucket.Object(key)
        return obj.get()['Body'].read()

def get_storage_backend() -> StorageBackend:
    import os
    backend_type = os.getenv('STORAGE_BACKEND', 'local')
    if backend_type == 'local':
        return LocalFileSystemBackend('/tmp/storage')
    elif backend_type == 's3':
        return S3Backend(bucket_name='my-bucket',
                         aws_access_key_id='your-access-key-id',
                         aws_secret_access_key='your-secret-access-key')
    else:
        raise ValueError(f'Unknown storage backend type: {backend_type}')