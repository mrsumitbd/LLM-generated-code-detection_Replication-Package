def create_server_config_from_params(
    name: str,
    server_type: str,
    command: Optional[str] = None,
    args: Optional[str] = None,
    env: Optional[str] = None,
    url: Optional[str] = None,
    headers: Optional[str] = None,
) -> Dict:
    """
    Create a server configuration dictionary from CLI parameters.

    Args:
        name: Server name
        server_type: Server type ("stdio" or "remote")
        command: Command for stdio servers
        args: Command arguments
        env: Environment variables
        url: URL for remote servers
        headers: HTTP headers for remote servers

    Returns:
        Server configuration dictionary

    Raises:
        ValueError: If parameters are invalid
    """
    if not name:
        raise ValueError("Server name is required")
    
    if server_type not in ("stdio", "remote"):
        raise ValueError(f"Invalid server type: {server_type}. Must be 'stdio' or 'remote'")
    
    config = {
        "name": name,
        "type": server_type,
    }
    
    if server_type == "stdio":
        if not command:
            raise ValueError("Command is required for stdio servers")
        config["command"] = command
        
        if args:
            config["args"] = args.split()
        
        if env:
            env_dict = {}
            for item in env.split(","):
                item = item.strip()
                if "=" in item:
                    key, value = item.split("=", 1)
                    env_dict[key.strip()] = value.strip()
            if env_dict:
                config["env"] = env_dict
    
    elif server_type == "remote":
        if not url:
            raise ValueError("URL is required for remote servers")
        config["url"] = url
        
        if headers:
            headers_dict = {}
            for item in headers.split(","):
                item = item.strip()
                if ":" in item:
                    key, value = item.split(":", 1)
                    headers_dict[key.strip()] = value.strip()
            if headers_dict:
                config["headers"] = headers_dict
    
    return config