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
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary")
    
    if storage_type == "local":
        if "path" not in config:
            raise ValueError("Local storage requires 'path' configuration")
        if not isinstance(config["path"], str):
            raise ValueError("'path' must be a string")
        if not config["path"]:
            raise ValueError("'path' cannot be empty")
        return True
    
    elif storage_type == "s3":
        required_keys = {"bucket", "region"}
        missing_keys = required_keys - set(config.keys())
        if missing_keys:
            raise ValueError(f"S3 storage requires {missing_keys} configuration")
        if not isinstance(config["bucket"], str) or not config["bucket"]:
            raise ValueError("'bucket' must be a non-empty string")
        if not isinstance(config["region"], str) or not config["region"]:
            raise ValueError("'region' must be a non-empty string")
        if "access_key" in config and not isinstance(config["access_key"], str):
            raise ValueError("'access_key' must be a string")
        if "secret_key" in config and not isinstance(config["secret_key"], str):
            raise ValueError("'secret_key' must be a string")
        return True
    
    elif storage_type == "azure":
        required_keys = {"container", "account_name"}
        missing_keys = required_keys - set(config.keys())
        if missing_keys:
            raise ValueError(f"Azure storage requires {missing_keys} configuration")
        if not isinstance(config["container"], str) or not config["container"]:
            raise ValueError("'container' must be a non-empty string")
        if not isinstance(config["account_name"], str) or not config["account_name"]:
            raise ValueError("'account_name' must be a non-empty string")
        if "account_key" in config and not isinstance(config["account_key"], str):
            raise ValueError("'account_key' must be a string")
        return True
    
    elif storage_type == "gcs":
        required_keys = {"bucket", "project_id"}
        missing_keys = required_keys - set(config.keys())
        if missing_keys:
            raise ValueError(f"GCS storage requires {missing_keys} configuration")
        if not isinstance(config["bucket"], str) or not config["bucket"]:
            raise ValueError("'bucket' must be a non-empty string")
        if not isinstance(config["project_id"], str) or not config["project_id"]:
            raise ValueError("'project_id' must be a non-empty string")
        if "credentials_path" in config and not isinstance(config["credentials_path"], str):
            raise ValueError("'credentials_path' must be a string")
        return True
    
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")