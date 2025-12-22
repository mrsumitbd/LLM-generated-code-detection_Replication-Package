from typing import Dict, Optional
from bedrock_server_manager.api.utils import server_lifecycle_manager
from bedrock_server_manager.core.bedrock_server import BedrockServer
from bedrock_server_manager.exceptions import (
    InvalidServerNameError,
    UserInputError,
    AppFileNotFoundError,
    FileOperationError,
    ServerStopError,
    ServerStartError,
)
from bedrock_server_manager.api.plugin_events import (
    before_properties_change,
    after_properties_change,
)
from bedrock_server_manager.api.types import AppContext

def modify_server_properties(
    server_name: str,
    properties_to_update: Dict[str, str],
    restart_after_modify: bool = False,
    app_context: Optional[AppContext] = None,
) -> Dict[str, str]:
    # Validate server name
    if not server_name:
        raise InvalidServerNameError("Server name cannot be empty.")

    # Validate properties_to_update
    if not isinstance(properties_to_update, dict):
        raise TypeError("properties_to_update must be a dictionary.")

    # Validate each property value
    for prop, value in properties_to_update.items():
        try:
            validate_server_property_value(prop, value)
        except UserInputError as e:
            return {"status": "error", "message": str(e)}

    # Trigger before_properties_change event
    before_properties_change.send(server_name, properties_to_update)

    # Manage server lifecycle
    with server_lifecycle_manager(server_name, restart_after_modify, app_context):
        server = BedrockServer(server_name, app_context)
        for prop, value in properties_to_update.items():
            server.set_server_property(prop, value)

    # Trigger after_properties_change event
    after_properties_change.send(server_name, properties_to_update)

    return {"status": "success", "message": "Server properties updated successfully."}

def validate_server_property_value(prop: str, value: str) -> None:
    # Implement property value validation logic here
    pass