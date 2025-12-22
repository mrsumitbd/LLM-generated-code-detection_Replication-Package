from typing import Any, Dict, List

# The following imports assume that the relevant classes are defined elsewhere
# in the same package or are otherwise importable.
from .base_check import BaseCheck
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
        Create a single BaseCheck instance from a configuration dictionary.

        Parameters
        ----------
        config_data : Dict[str, Any]
            Dictionary containing configuration for a check. Must include a
            ``type`` key that identifies the concrete check class.

        Returns
        -------
        BaseCheck
            An instantiated check object.

        Raises
        ------
        ValueError
            If the configuration is missing the ``type`` key or if the type
            cannot be resolved to a concrete check class.
        """
        if not isinstance(config_data, dict):
            raise ValueError("Configuration must be a dictionary")

        # Extract the type identifier
        check_type = config_data.pop("type", None)
        if check_type is None:
            raise ValueError("Configuration dictionary must contain a 'type' key")

        # Resolve the concrete check class from the registry
        check_cls = CheckConfigRegistry.get_check_class(check_type)
        if check_cls is None:
            raise ValueError(f"Unknown check type '{check_type}'")

        # Instantiate the check with the remaining configuration parameters
        try:
            check_instance = check_cls(**config_data)
        except TypeError as exc:
            raise ValueError(
                f"Failed to instantiate check '{check_type}': {exc}"
            ) from exc

        if not isinstance(check_instance, BaseCheck):
            raise ValueError(
                f"Instantiated object of type '{check_type}' does not "
                f"inherit from BaseCheck"
            )

        return check_instance

    @staticmethod
    def from_list(config_list: List[Dict[str, Any]]) -> List[BaseCheck]:
        """
        Convert a list of configuration dictionaries into a list of check instances.

        Parameters
        ----------
        config_list : List[Dict[str, Any]]
            List of configuration dictionaries, each describing a check.

        Returns
        -------
        List[BaseCheck]
            List of instantiated check objects.
        """
        if not isinstance(config_list, list):
            raise ValueError("Configuration list must be a list of dictionaries")

        checks: List[BaseCheck] = []
        for idx, cfg in enumerate(config_list):
            try:
                check = CheckFactory._from_dict(cfg.copy())
                checks.append(check)
            except Exception as exc:
                raise ValueError(
                    f"Error processing configuration at index {idx}: {exc}"
                ) from exc

        return checks