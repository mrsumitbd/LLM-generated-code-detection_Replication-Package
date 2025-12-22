from typing import Dict, Optional

# Import the required classes and exceptions.  The exact import paths may vary
# depending on the project layout, but the following are the most common
# locations for these objects in the Bedrock-Server project.
try:
    from .core.bedrock_server import BedrockServer
    from .core.app_context import AppContext
    from .core.exceptions import (
        InvalidServerNameError,
        MissingArgumentError,
        UserInputError,
        FileOperationError,
        ConfigParseError,
    )
except Exception:  # pragma: no cover
    # Fallback imports for environments where the relative imports fail
    from core.bedrock_server import BedrockServer
    from core.app_context import AppContext
    from core.exceptions import (
        InvalidServerNameError,
        MissingArgumentError,
        UserInputError,
        FileOperationError,
        ConfigParseError,
    )


def set_autostart(
    server_name: str,
    autostart_value: str,
    app_context: Optional[AppContext] = None,
) -> Dict[str, str]:
    """
    Sets the 'autostart' flag in the server's specific JSON configuration file.

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
    # Validate input arguments
    if not server_name:
        raise InvalidServerNameError("Server name must be provided.")
    if not autostart_value:
        raise MissingArgumentError("Autostart value must be provided.")

    # Normalize and validate the autostart value
    value_lower = autostart_value.strip().lower()
    if value_lower not in ("true", "false"):
        raise UserInputError(
            "Autostart value must be 'true' or 'false' (case-insensitive)."
        )
    bool_value = value_lower == "true"

    # Obtain the application context
    if app_context is None:
        app_context = AppContext.get_instance()

    # Instantiate the BedrockServer object
    server = BedrockServer(server_name, app_context)

    # Trigger the before event
    try:
        app_context.plugin_manager.trigger(
            "before_autostart_change",
            server_name=server_name,
            autostart=bool_value,
        )
    except Exception:  # pragma: no cover
        # If plugin events fail, we still want to proceed with the change
        pass

    # Perform the actual autostart change
    try:
        server.set_autostart(bool_value)
    except (FileOperationError, ConfigParseError) as exc:
        # Return an error dictionary instead of raising
        return {
            "status": "error",
            "message": f"Failed to update autostart setting: {str(exc)}",
        }

    # Trigger the after event
    try:
        app_context.plugin_manager.trigger(
            "after_autostart_change",
            server_name=server_name,
            autostart=bool_value,
        )
    except Exception:  # pragma: no cover
        # Ignore plugin errors after the change
        pass

    # Return success message
    return {
        "status": "success",
        "message": f"autostart setting for '{server_name}' updated to {bool_value}.",
    }