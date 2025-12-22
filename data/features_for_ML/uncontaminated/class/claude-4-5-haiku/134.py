class BaseConfig:

    @staticmethod
    def from_dict(config_class, config_dict):
        """Create an instance of config_class from a dictionary."""
        if not isinstance(config_dict, dict):
            raise TypeError(f"config_dict must be a dictionary, got {type(config_dict)}")
        
        # Get the __init__ signature to determine valid parameters
        import inspect
        sig = inspect.signature(config_class.__init__)
        
        # Filter config_dict to only include parameters that __init__ accepts
        valid_params = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param_name in config_dict:
                valid_params[param_name] = config_dict[param_name]
        
        # Create and return instance with filtered parameters
        return config_class(**valid_params)