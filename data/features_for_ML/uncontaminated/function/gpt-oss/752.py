import json
import shlex
from typing import Dict, Optional, List, Any


def _parse_args(args_str: str) -> List[str]:
    """Parse a string of arguments into a list."""
    if not args_str or not args_str.strip():
        return []
    args_str = args_str.strip()
    # Try JSON parsing first
    if args_str[0] in ("[", "{"):
        try:
            parsed = json.loads(args_str)
            if isinstance(parsed, list):
                return [str(x) for x in parsed]
            if isinstance(parsed, dict):
                # If a dict is provided, treat its values as args
                return [str(v) for v in parsed.values()]
        except json.JSONDecodeError:
            pass
    # Fallback to shell-like splitting
    return shlex.split(args_str)


def _parse_kv_pairs(kv_str: str, sep: str = "=") -> Dict[str, str]:
    """Parse comma-separated key{sep}value pairs into a dict."""
    result: Dict[str, str] = {}
    if not kv_str or not kv_str.strip():
        return result
    for part in kv_str.split(","):
        part = part.strip()
        if not part:
            continue
        if sep not in part:
            raise ValueError(f"Invalid key{sep}value pair: '{part}'")
        key, value = part.split(sep, 1)
        result[key.strip()] = value.strip()
    return result


def _parse_headers(headers_str: str) -> Dict[str, str]:
    """Parse comma-separated 'Header: Value' pairs into a dict."""
    return _parse_kv_pairs(headers_str, sep=":")


def create_server_config_from_params(
    name: str,
    server_type: str,
    command: Optional[str] = None,
    args: Optional[str] = None,
    env: Optional[str] = None,
    url: Optional[str] = None,
    headers: Optional[str] = None,
) -> Dict[str, Any]:
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
        raise ValueError("Server name must be provided")

    server_type = server_type.lower()
    if server_type not in {"stdio", "remote"}:
        raise ValueError(f"Invalid server_type '{server_type}'. Must be 'stdio' or 'remote'")

    config: Dict[str, Any] = {"name": name, "type": server_type}

    if server_type == "stdio":
        if not command:
            raise ValueError("Command must be provided for stdio server_type")
        cmd_list = [command]
        cmd_args = _parse_args(args) if args else []
        cmd_list.extend(cmd_args)
        config["command"] = cmd_list
        env_dict = _parse_kv_pairs(env) if env else {}
        if env_dict:
            config["env"] = env_dict
    else:  # remote
        if not url:
            raise ValueError("URL must be provided for remote server_type")
        config["url"] = url
        headers_dict = _parse_headers(headers) if headers else {}
        if headers_dict:
            config["headers"] = headers_dict

    return config