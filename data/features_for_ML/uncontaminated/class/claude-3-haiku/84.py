from typing import Dict, Any, List
from .base import BaseCheck
from .registry import CheckConfigRegistry

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
        Instantiate a single check from the provided configuration dictionary.

        Args:
            config_data (Dict[str, Any]): Configuration data for the check.

        Returns:
            BaseCheck: An instance of the check implementation.
        """
        check_type = config_data.get('type')
        if not check_type:
            raise ValueError("Configuration data must contain a 'type' field.")

        check_config = CheckConfigRegistry.get_config(check_type)
        if not check_config:
            raise ValueError(f"No registered configuration for check type '{check_type}'.")

        check_params = check_config.validate_params(config_data)
        return check_config.create_instance(**check_params)

    @staticmethod
    def from_list(config_list: List[Dict[str, Any]]) -> List[BaseCheck]:
        """
        Instantiate a list of checks from the provided configuration data.

        Args:
            config_list (List[Dict[str, Any]]): List of configuration dictionaries.

        Returns:
            List[BaseCheck]: List of check instances.
        """
        return [CheckFactory._from_dict(config) for config in config_list]