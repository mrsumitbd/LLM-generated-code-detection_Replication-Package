class Config:
    """Config for an imaginaire4 job.

    See /README.md/Configuration System for more info.
    """

    def __init__(self, config_dict: dict[str, Any] | None = None):
        """Initialize Config from dictionary."""
        self._config = config_dict or {}

    def pretty_print(self, use_color: bool = False) -> str:
        """Return a pretty-printed string representation of the config.
        
        Args:
            use_color: Whether to use ANSI color codes in output.
            
        Returns:
            A formatted string representation of the configuration.
        """
        def format_value(value, indent=0):
            """Recursively format values with proper indentation."""
            spaces = "  " * indent
            
            if isinstance(value, dict):
                if not value:
                    return "{}"
                items = []
                for k, v in value.items():
                    formatted_v = format_value(v, indent + 1)
                    items.append(f"{spaces}  {k}: {formatted_v}")
                return "{\n" + "\n".join(items) + f"\n{spaces}}}"
            elif isinstance(value, list):
                if not value:
                    return "[]"
                items = []
                for item in value:
                    formatted_item = format_value(item, indent + 1)
                    items.append(f"{spaces}  - {formatted_item}")
                return "[\n" + "\n".join(items) + f"\n{spaces}]"
            elif isinstance(value, str):
                if use_color:
                    return f"\033[92m'{value}'\033[0m"
                return f"'{value}'"
            elif isinstance(value, bool):
                if use_color:
                    return f"\033[94m{value}\033[0m"
                return str(value)
            elif isinstance(value, (int, float)):
                if use_color:
                    return f"\033[93m{value}\033[0m"
                return str(value)
            else:
                return str(value)
        
        return format_value(self._config)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary representation.
        
        Returns:
            Dictionary representation of the configuration.
        """
        def deep_copy_dict(d):
            """Recursively copy dictionary."""
            if isinstance(d, dict):
                return {k: deep_copy_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [deep_copy_dict(item) for item in d]
            else:
                return d
        
        return deep_copy_dict(self._config)

    def validate(self) -> None:
        """Validate the configuration.
        
        Raises:
            ValueError: If configuration is invalid.
        """
        if not isinstance(self._config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        # Check for required top-level keys if needed
        # This can be extended based on specific requirements
        
        # Recursively validate nested structures
        def validate_structure(obj, path=""):
            """Recursively validate configuration structure."""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if not isinstance(key, str):
                        raise ValueError(f"Dictionary keys must be strings at {path}")
                    validate_structure(value, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    validate_structure(item, f"{path}[{i}]")
            elif obj is None or isinstance(obj, (str, int, float, bool)):
                pass
            else:
                raise ValueError(f"Invalid type {type(obj)} at {path}")
        
        validate_structure(self._config)