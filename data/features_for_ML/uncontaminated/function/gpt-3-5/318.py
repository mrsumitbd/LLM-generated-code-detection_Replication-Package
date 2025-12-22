def validate_storage_config(storage_type: str, config: Dict[str, Any]) -> bool:
    if storage_type == "local":
        if "path" not in config:
            raise ValueError("Path is required for local storage configuration")
    elif storage_type == "s3":
        if "bucket" not in config:
            raise ValueError("Bucket is required for S3 storage configuration")
    elif storage_type == "azure":
        if "account_name" not in config or "container" not in config:
            raise ValueError("Account name and container are required for Azure storage configuration")
    else:
        raise ValueError("Invalid storage type provided")
    
    return True