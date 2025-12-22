from typing import Dict, List, Optional

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
    # Validate server type
    server_type = validate_server_type(server_type)

    # Validate required parameters
    validate_required_for_type(server_type, command=command, url=url)

    # Base configuration
    config = {
        "name": name,
        "type": server_type,
    }

    if server_type == "stdio":
        config["command"] = command
        if args:
            config["args"] = args.split()
        # Add environment variables if provided (stdio servers only)
        if env:
            config["env"] = parse_key_value_pairs(env)
    elif server_type == "remote":
        config["url"] = url
        if headers:
            config["headers"] = parse_header_pairs(headers)
        # Remote servers don't support environment variables
        if env:
            raise ValueError("Environment variables are not supported for remote servers")

    return config