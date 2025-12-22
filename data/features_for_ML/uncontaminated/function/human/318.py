from typing import Any, Dict

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
    storage_type = storage_type.lower()
    
    if storage_type == "memory":
        # Memory storage has minimal configuration requirements
        return True
    
    elif storage_type == "sqlite":
        required_fields = ["database_path"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"SQLite storage missing required field: {field}")
        return True
    
    elif storage_type == "postgresql":
        required_fields = ["host", "database", "username", "password"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"PostgreSQL storage missing required field: {field}")
        return True
    
    elif storage_type == "s3":
        required_fields = ["bucket_name"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"S3 storage missing required field: {field}")
        return True
    
    elif storage_type == "redis":
        # Redis has sensible defaults for all fields
        return True
    
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")