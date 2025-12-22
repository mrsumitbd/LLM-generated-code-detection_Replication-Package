import importlib
import logging

def module_checker(class_name: str) -> None:
    """
    Checks if required config plugins are present before running the ARES pipeline.

    This function verifies the presence of a specified plugin before proceeding with the ARES pipeline execution.

    :param class_name: The name of the plugin to check for.
    """
    try:
        importlib.import_module(class_name)
    except ImportError:
        logging.error(f"The required plugin '{class_name}' is not installed or available. Please install the necessary dependencies and try again.")
        raise ImportError(f"The required plugin '{class_name}' is not installed or available.")