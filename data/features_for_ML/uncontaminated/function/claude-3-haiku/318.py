def validate_storage_config(storage_type: str, config: Dict[str, Any]) -> bool:
    """
    Validate storage configuration for a given type.
    
    Args:
        storage_type: Storage type to validate
        config: Configuration to validate
        
    Returns:
        True if configuration is valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    if storage_type == "local":
        if "path" not in config or not isinstance(config["path"], str):
            raise ValueError("Invalid local storage configuration: 'path' is required and must be a string.")
        if "permissions" in config and not isinstance(config["permissions"], int):
            raise ValueError("Invalid local storage configuration: 'permissions' must be an integer.")
        return True
    elif storage_type == "s3":
        if "bucket" not in config or not isinstance(config["bucket"], str):
            raise ValueError("Invalid S3 storage configuration: 'bucket' is required and must be a string.")
        if "access_key" not in config or not isinstance(config["access_key"], str):
            raise ValueError("Invalid S3 storage configuration: 'access_key' is required and must be a string.")
        if "secret_key" not in config or not isinstance(config["secret_key"], str):
            raise ValueError("Invalid S3 storage configuration: 'secret_key' is required and must be a string.")
        return True
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")