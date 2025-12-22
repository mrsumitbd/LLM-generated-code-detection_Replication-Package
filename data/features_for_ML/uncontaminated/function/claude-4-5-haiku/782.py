def modify_server_properties(
    server_name: str,
    properties_to_update: Dict[str, str],
    restart_after_modify: bool = False,
    app_context: Optional[AppContext] = None,
) -> Dict[str, str]:
    """Modifies one or more properties in `server.properties`."""
    
    # Validate server_name
    if not server_name or not isinstance(server_name, str):
        raise InvalidServerNameError("Server name cannot be empty")
    
    # Validate properties_to_update is a dictionary
    if not isinstance(properties_to_update, dict):
        raise TypeError("properties_to_update must be a dictionary")
    
    # Get app context if not provided
    if app_context is None:
        app_context = AppContext.get_instance()
    
    # Get the server instance
    server = app_context.get_server(server_name)
    
    # Validate all properties before making any changes
    for prop_key, prop_value in properties_to_update.items():
        validate_server_property_value(prop_key, prop_value)
    
    # Trigger before_properties_change event
    app_context.plugin_manager.trigger_event(
        "before_properties_change",
        server_name=server_name,
        properties=properties_to_update
    )
    
    try:
        # Use server lifecycle manager to handle server state
        with server_lifecycle_manager(
            server=server,
            should_stop=restart_after_modify,
            should_start=restart_after_modify
        ):
            # Apply each property change
            for prop_key, prop_value in properties_to_update.items():
                server.set_server_property(prop_key, prop_value)
        
        # Trigger after_properties_change event
        app_context.plugin_manager.trigger_event(
            "after_properties_change",
            server_name=server_name,
            properties=properties_to_update
        )
        
        return {
            "status": "success",
            "message": "Server properties updated successfully."
        }
    
    except (InvalidServerNameError, UserInputError, AppFileNotFoundError, 
            FileOperationError, ServerStopError, ServerStartError) as e:
        return {
            "status": "error",
            "message": str(e)
        }