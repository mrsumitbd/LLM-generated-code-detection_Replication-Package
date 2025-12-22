def get_storage_backend() -> StorageBackend:
    """Get the configured storage backend instance."""
    backend_type = os.getenv('STORAGE_BACKEND', 'local').lower()
    
    if backend_type == 's3':
        return S3StorageBackend(
            bucket=os.getenv('S3_BUCKET'),
            region=os.getenv('S3_REGION', 'us-east-1'),
            access_key=os.getenv('S3_ACCESS_KEY'),
            secret_key=os.getenv('S3_SECRET_KEY')
        )
    elif backend_type == 'gcs':
        return GCSStorageBackend(
            bucket=os.getenv('GCS_BUCKET'),
            project_id=os.getenv('GCS_PROJECT_ID'),
            credentials_path=os.getenv('GCS_CREDENTIALS_PATH')
        )
    elif backend_type == 'azure':
        return AzureStorageBackend(
            container=os.getenv('AZURE_CONTAINER'),
            account_name=os.getenv('AZURE_ACCOUNT_NAME'),
            account_key=os.getenv('AZURE_ACCOUNT_KEY')
        )
    else:
        return LocalStorageBackend(
            base_path=os.getenv('LOCAL_STORAGE_PATH', './storage')
        )