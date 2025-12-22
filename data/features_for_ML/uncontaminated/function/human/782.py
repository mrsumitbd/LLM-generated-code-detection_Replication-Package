from typing import Dict, List, Optional, Any
from ..instances import (
    get_server_instance,
    get_settings_instance,
)
from .utils import (
    server_lifecycle_manager,
    validate_server_name_format,
)
from ..error import (
    BSMError,
    InvalidServerNameError,
    FileOperationError,
    MissingArgumentError,
    UserInputError,
    AppFileNotFoundError,
)
from ..context import AppContext

def modify_server_properties(
    server_name: str,
    properties_to_update: Dict[str, str],
    restart_after_modify: bool = False,
    app_context: Optional[AppContext] = None,
) -> Dict[str, str]:
    """Modifies one or more properties in `server.properties`.

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
    if not server_name:
        raise InvalidServerNameError("Server name required.")
    if not isinstance(properties_to_update, dict):
        raise TypeError("Properties must be a dict.")

    try:
        # First, validate all properties before making any changes.
        for name, val_str in properties_to_update.items():
            val_res = validate_server_property_value(
                name, str(val_str) if val_str is not None else ""
            )
            if val_res.get("status") == "error":
                raise UserInputError(
                    f"Validation failed for '{name}': {val_res.get('message')}"
                )

        # Use a context manager to handle stopping and restarting the server.
        with server_lifecycle_manager(
            server_name,
            stop_before=restart_after_modify,
            restart_on_success_only=True,
            app_context=app_context,
        ):
            if app_context:
                server = app_context.get_server(server_name)
            else:
                server = get_server_instance(server_name)
            for prop_name, prop_value in properties_to_update.items():
                server.set_server_property(prop_name, prop_value)

        return {
            "status": "success",
            "message": "Server properties updated successfully.",
        }

    except (BSMError, FileNotFoundError, UserInputError) as e:
        logger.error(
            f"API: Failed to modify properties for '{server_name}': {e}", exc_info=True
        )
        return {"status": "error", "message": f"Failed to modify properties: {e}"}
    except Exception as e:
        logger.error(
            f"API: Unexpected error modifying properties for '{server_name}': {e}",
            exc_info=True,
        )
        return {"status": "error", "message": f"Unexpected error: {e}"}