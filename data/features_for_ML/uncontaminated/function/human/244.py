from ..error import (
    BSMError,
    InvalidServerNameError,
    MissingArgumentError,
    UserInputError,
)
from typing import Dict, Any, Optional
from ..instances import get_server_instance
from ..context import AppContext

def set_autostart(
    server_name: str, autostart_value: str, app_context: Optional[AppContext] = None
) -> Dict[str, str]:
    """Sets the 'autostart' flag in the server's specific JSON configuration file.

    This function modifies the server-specific JSON configuration file to
    enable or disable the automatic update check before the server starts,
    by calling :meth:`~.core.bedrock_server.BedrockServer.set_autostart`.
    Triggers ``before_autostart_change`` and ``after_autostart_change`` plugin events.

    Args:
        server_name (str): The name of the server.
        autostart_value (str): The desired state for autostart.
            Must be 'true' or 'false' (case-insensitive).

    Returns:
        Dict[str, str]: A dictionary with the operation result.
        On success: ``{"status": "success", "message": "autostart setting for '<name>' updated to <bool_value>."}``
        On error: ``{"status": "error", "message": "<error_message>"}``

    Raises:
        InvalidServerNameError: If `server_name` is not provided.
        MissingArgumentError: If `autostart_value` is not provided.
        UserInputError: If `autostart_value` is not 'true' or 'false'.
        FileOperationError: If writing the server's JSON configuration file fails.
        ConfigParseError: If the server's JSON configuration is malformed during load/save.
    """
    if not server_name:
        raise InvalidServerNameError("Server name cannot be empty.")
    if autostart_value is None:
        raise MissingArgumentError("autostart value cannot be empty.")

    # Validate and convert the input string to a boolean.
    value_lower = str(autostart_value).lower()
    if value_lower not in ("true", "false"):
        raise UserInputError("autostart value must be 'true' or 'false'.")
    value_bool = value_lower == "true"

    try:
        logger.info(
            f"API: Setting 'autostart' config for server '{server_name}' to {value_bool}..."
        )
        if app_context:
            server = app_context.get_server(server_name)
        else:
            server = get_server_instance(server_name)
        server.set_autostart(value_bool)
        return {
            "status": "success",
            "message": f"autostart setting for '{server_name}' updated to {value_bool}.",
        }

    except BSMError as e:
        logger.error(
            f"API: Failed to set autostart config for '{server_name}': {e}",
            exc_info=True,
        )
        return {"status": "error", "message": f"Failed to set autostart config: {e}"}
    except Exception as e:
        logger.error(
            f"API: Unexpected error setting autostart for '{server_name}': {e}",
            exc_info=True,
        )
        return {
            "status": "error",
            "message": f"Unexpected error setting autostart: {e}",
        }