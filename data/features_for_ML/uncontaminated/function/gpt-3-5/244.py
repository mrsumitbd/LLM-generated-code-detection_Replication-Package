from typing import Dict, Optional

def set_autostart(
    server_name: str, autostart_value: str, app_context: Optional[AppContext] = None
) -> Dict[str, str]:
    if not server_name:
        raise InvalidServerNameError("Server name is required.")
    if not autostart_value:
        raise MissingArgumentError("Autostart value is required.")
    if autostart_value.lower() not in ['true', 'false']:
        raise UserInputError("Autostart value must be 'true' or 'false'.")

    try:
        # Code to modify the server-specific JSON configuration file
        # Call BedrockServer.set_autostart method
        # Trigger before_autostart_change and after_autostart_change plugin events

        return {"status": "success", "message": f"autostart setting for '{server_name}' updated to {autostart_value}."}
    except Exception as e:
        return {"status": "error", "message": str(e)}