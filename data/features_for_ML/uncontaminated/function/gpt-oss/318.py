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
    if not isinstance(storage_type, str):
        raise ValueError("storage_type must be a string")

    if not isinstance(config, dict):
        raise ValueError("config must be a dictionary")

    # Helper to check required keys and types
    def _require(keys: Dict[str, type], cfg: Dict[str, Any], prefix: str = ""):
        for key, typ in keys.items():
            if key not in cfg:
                raise ValueError(f"{prefix}{key!r} is required for {storage_type!r}")
            if not isinstance(cfg[key], typ):
                raise ValueError(f"{prefix}{key!r} must be of type {typ.__name__}")

    # Define required fields per storage type
    if storage_type.lower() == "s3":
        _require(
            {
                "bucket": str,
                "region": str,
                "access_key": str,
                "secret_key": str,
            },
            config,
            prefix="s3 config: ",
        )
        # Optional endpoint_url must be string if present
        if "endpoint_url" in config and not isinstance(config["endpoint_url"], str):
            raise ValueError("s3 config: endpoint_url must be a string")

    elif storage_type.lower() == "gcs":
        _require(
            {
                "bucket": str,
                "credentials_json": str,
            },
            config,
            prefix="gcs config: ",
        )

    elif storage_type.lower() == "azure":
        _require(
            {
                "container": str,
                "account_name": str,
                "account_key": str,
            },
            config,
            prefix="azure config: ",
        )

    elif storage_type.lower() == "local":
        _require(
            {
                "path": str,
            },
            config,
            prefix="local config: ",
        )

    elif storage_type.lower() == "hdfs":
        _require(
            {
                "host": str,
                "port": int,
                "user": str,
            },
            config,
            prefix="hdfs config: ",
        )

    else:
        raise ValueError(f"Unsupported storage_type: {storage_type!r}")

    return True