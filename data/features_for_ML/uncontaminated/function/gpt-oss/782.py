from typing import Dict, Optional

# Import the utilities and exceptions that are expected to exist in the package.
# These imports are written in a defensive way so that the module can be imported
# even if the optional dependencies are missing – the actual implementation
# will only be executed when the function is called.
try:
    from bedrock_server_manager.api.utils.server_lifecycle_manager import (
        server_lifecycle_manager,
    )
    from bedrock_server_manager.core.bedrock_server import BedrockServer
    from bedrock_server_manager.api.exceptions import (
        InvalidServerNameError,
        UserInputError,
        AppFileNotFoundError,
        FileOperationError,
        ServerStopError,
        ServerStartError,
    )
    from bedrock_server_manager.api.utils.validation import validate_server_property_value
    from bedrock_server_manager.api.plugins import trigger_event
except Exception:  # pragma: no cover
    # If any of the imports fail, we still want the module to be importable.
    # The function will raise an ImportError when called.
    pass


def modify_server_properties(
    server_name: str,
    properties_to_update: Dict[str, str],
    restart_after_modify: bool = False,
    app_context: Optional["AppContext"] = None,
) -> Dict[str, str]:
    """
    Modifies one or more properties in `server.properties`.

    This function first validates all provided properties using
    :func:`~.validate_server_property_value`. If all validations pass, it
    then uses the :func:`~bedrock_server_manager.api.utils.server_lifecycle_manager`
    to manage the server's state (stopping it if `restart_after_modify` is ``True``).
    Within the managed context, it applies each change by calling
    :meth:`~.core.bedrock_server.BedrockServer.set_server_property`.
    If `restart_after_modify` is ``True``, the server is restarted only if all
    properties are successfully set and the lifecycle manager completes without error.
    Triggers ``before_properties_change`` and ``after_properties_change`` plugin events.

    Args:
        server_name (str): The name of the server to modify.
        properties_to_update (Dict[str, str]): A dictionary of property keys
            and their new string values.
        restart_after_modify (bool, optional): If ``True``, the server will be
            stopped before applying changes and restarted afterwards if successful.
            Defaults to ``True``.

    Returns:
        Dict[str, str]: A dictionary with the operation result.
        On success: ``{"status": "success", "message": "Server properties updated successfully."}``
        On error (validation, file op, etc.): ``{"status": "error", "message": "<error_message>"}``

    Raises:
        InvalidServerNameError: If `server_name` is empty.
        TypeError: If `properties_to_update` is not a dictionary.
        UserInputError: If any property value fails validation via
            :func:`~.validate_server_property_value` or contains invalid characters.
        AppFileNotFoundError: If ``server.properties`` does not exist.
        FileOperationError: If reading/writing ``server.properties`` fails.
        ServerStopError/ServerStartError: If server stop/start fails during lifecycle management.
    """
    # Basic argument validation
    if not isinstance(server_name, str) or not server_name.strip():
        raise InvalidServerNameError("Server name must be a non-empty string.")
    if not isinstance(properties_to_update, dict):
        raise TypeError("properties_to_update must be a dictionary.")

    # Validate each property value
    for key, value in properties_to_update.items():
        try:
            validate_server_property_value(key, value)
        except Exception as exc:
            raise UserInputError(f"Invalid value for property '{key}': {exc}") from exc

    # Prepare the BedrockServer instance
    server = BedrockServer(server_name, app_context=app_context)

    # Use the lifecycle manager to handle stop/start if requested
    try:
        with server_lifecycle_manager(server, restart_after_modify=restart_after_modify):
            # Trigger before change event
            trigger_event("before_properties_change", server_name=server_name, changes=properties_to_update)

            # Apply each property change
            for key, value in properties_to_update.items():
                server.set_server_property(key, value)

            # Trigger after change event
            trigger_event("after_properties_change", server_name=server_name, changes=properties_to_update)

    except (ServerStopError, ServerStartError) as exc:
        # Lifecycle errors are propagated as is
        raise
    except FileOperationError as exc:
        # File operation errors are propagated as is
        raise
    except AppFileNotFoundError as exc:
        # File not found errors are propagated as is
        raise
    except Exception as exc:
        # Any other exception is treated as a generic error
        return {"status": "error", "message": f"Unexpected error: {exc}"}

    # If we reach here, everything succeeded
    return {
        "status": "success",
        "message": "Server properties updated successfully.",
    }