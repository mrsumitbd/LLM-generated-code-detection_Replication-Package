def set_autostart(
    server_name: str, autostart_value: str, app_context: Optional[AppContext] = None
) -> Dict[str, str]:
    """Sets the 'autostart' flag in the server's specific JSON configuration file."""
    try:
        if not server_name:
            raise InvalidServerNameError("Server name is required.")

        if not autostart_value:
            raise MissingArgumentError("Autostart value is required.")

        autostart_value = autostart_value.lower()
        if autostart_value not in ("true", "false"):
            raise UserInputError("Autostart value must be 'true' or 'false'.")

        server = app_context.get_server(server_name)
        server.set_autostart(autostart_value == "true")

        return {
            "status": "success",
            "message": f"Autostart setting for '{server_name}' updated to {autostart_value}.",
        }
    except (
        InvalidServerNameError,
        MissingArgumentError,
        UserInputError,
        FileOperationError,
        ConfigParseError,
    ) as e:
        return {"status": "error", "message": str(e)}