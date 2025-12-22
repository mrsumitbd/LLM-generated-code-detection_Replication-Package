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
    from ._context import get_app_context
    from .exceptions import (
        InvalidServerNameError,
        MissingArgumentError,
        UserInputError,
        FileOperationError,
        ConfigParseError,
    )

    if app_context is None:
        app_context = get_app_context()

    # Validate inputs
    if not server_name:
        raise InvalidServerNameError("server_name is required")

    if not autostart_value:
        raise MissingArgumentError("autostart_value is required")

    # Validate autostart_value
    autostart_lower = autostart_value.lower()
    if autostart_lower not in ("true", "false"):
        raise UserInputError(
            f"autostart_value must be 'true' or 'false', got '{autostart_value}'"
        )

    try:
        # Get the server instance
        server = app_context.get_server(server_name)

        # Trigger before event
        app_context.trigger_event("before_autostart_change", server_name=server_name)

        # Convert string to boolean
        bool_value = autostart_lower == "true"

        # Set autostart on the server
        server.set_autostart(bool_value)

        # Trigger after event
        app_context.trigger_event("after_autostart_change", server_name=server_name)

        return {
            "status": "success",
            "message": f"autostart setting for '{server_name}' updated to {bool_value}.",
        }

    except (FileOperationError, ConfigParseError):
        raise
    except InvalidServerNameError:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}