class CheckFactory:
    """
    Factory for dynamic check instantiation from configuration dictionaries.

    Orchestrates the complete process of transforming raw configuration data into
    executable check instances, including type resolution, parameter validation,
    and proper instantiation. The factory leverages the CheckConfigRegistry to
    maintain loose coupling between check implementations and their configurations.

    This design enables flexible deployment scenarios where validation rules can
    be externally defined and dynamically loaded from various sources including
    configuration files, databases, or API endpoints.
    """

    @staticmethod
    def _from_dict(config_data: Dict[str, Any]) -> BaseCheck:
        """
        Create a single check instance from a configuration dictionary.
        
        Args:
            config_data: Dictionary containing check configuration with 'type' and parameters
            
        Returns:
            BaseCheck: Instantiated check object
            
        Raises:
            ValueError: If check type is not found or configuration is invalid
            KeyError: If required configuration keys are missing
        """
        if not isinstance(config_data, dict):
            raise ValueError("Configuration data must be a dictionary")
        
        if 'type' not in config_data:
            raise KeyError("Configuration must contain 'type' key")
        
        check_type = config_data['type']
        
        # Get the check class from registry
        check_class = CheckConfigRegistry.get(check_type)
        
        if check_class is None:
            raise ValueError(f"Unknown check type: {check_type}")
        
        # Extract parameters (all keys except 'type')
        params = {k: v for k, v in config_data.items() if k != 'type'}
        
        # Instantiate the check with parameters
        try:
            check_instance = check_class(**params)
        except TypeError as e:
            raise ValueError(f"Invalid parameters for check type '{check_type}': {str(e)}")
        
        return check_instance

    @staticmethod
    def from_list(config_list: List[Dict[str, Any]]) -> List[BaseCheck]:
        """
        Create multiple check instances from a list of configuration dictionaries.
        
        Args:
            config_list: List of configuration dictionaries
            
        Returns:
            List[BaseCheck]: List of instantiated check objects
            
        Raises:
            ValueError: If config_list is not a list or contains invalid configurations
        """
        if not isinstance(config_list, list):
            raise ValueError("Configuration list must be a list")
        
        checks = []
        for idx, config_data in enumerate(config_list):
            try:
                check = CheckFactory._from_dict(config_data)
                checks.append(check)
            except (ValueError, KeyError, TypeError) as e:
                raise ValueError(f"Error creating check at index {idx}: {str(e)}")
        
        return checks