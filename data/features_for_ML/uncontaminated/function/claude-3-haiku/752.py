from typing import Dict, Optional

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
    if server_type not in ("stdio", "remote"):
        raise ValueError("Invalid server type. Must be 'stdio' or 'remote'.")

    config = {
        "name": name,
        "type": server_type,
    }

    if server_type == "stdio":
        if not command:
            raise ValueError("Command is required for stdio servers.")
        config["command"] = command
        if args:
            config["args"] = args
        if env:
            config["env"] = env
    elif server_type == "remote":
        if not url:
            raise ValueError("URL is required for remote servers.")
        config["url"] = url
        if headers:
            config["headers"] = headers

    return config