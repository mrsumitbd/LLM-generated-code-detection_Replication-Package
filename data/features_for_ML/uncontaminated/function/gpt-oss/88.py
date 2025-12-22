import importlib
import logging
from typing import Any

# Configure a module‑level logger
_logger = logging.getLogger(__name__)

def module_checker(class_name: str) -> None:
    """
    Checks if required config plugins are present before running the ARES pipeline.

    This function verifies the presence of a specified plugin before proceeding with the ARES pipeline execution.
    It attempts to import the module named ``class_name``. If the import fails, a RuntimeError is raised
    with a clear message indicating the missing plugin.

    Parameters
    ----------
    class_name : str
        The name of the plugin (module) to check for.
    """
    try:
        # Attempt to import the module. This will raise ImportError if the module cannot be found.
        importlib.import_module(class_name)
        _logger.debug("Successfully found plugin module '%s'.", class_name)
    except ImportError as exc:
        # Provide a more user‑friendly error message
        msg = (
            f"Required plugin '{class_name}' is missing. "
            f"Please install it before running the ARES pipeline."
        )
        _logger.error(msg)
        raise RuntimeError(msg) from exc