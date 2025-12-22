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
    if server_type not in ["stdio", "remote"]:
        raise ValueError("Invalid server type. Must be 'stdio' or 'remote'.")

    if server_type == "stdio":
        if not command:
            raise ValueError("Command is required for stdio servers.")
        config = {
            "name": name,
            "type": server_type,
            "command": command,
            "args": args,
            "env": env
        }
    else:
        if not url:
            raise ValueError("URL is required for remote servers.")
        config = {
            "name": name,
            "type": server_type,
            "url": url,
            "headers": headers
        }

    return config