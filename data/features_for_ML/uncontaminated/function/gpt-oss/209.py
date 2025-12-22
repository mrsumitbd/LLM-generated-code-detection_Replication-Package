import os
import json

def configure_server_properties(server_name, base_dir):
    """Configures common server properties interactively.

    Args:
        server_name (str): The name of the server.
        base_dir (str): The base directory where servers are stored.
    """
    # Ensure the server directory exists
    server_dir = os.path.join(base_dir, server_name)
    os.makedirs(server_dir, exist_ok=True)

    # Helper to get a value with a default
    def get_input(prompt, default=None, validator=None):
        while True:
            if default is not None:
                full_prompt = f"{prompt} [{default}]: "
            else:
                full_prompt = f"{prompt}: "
            value = input(full_prompt).strip()
            if not value and default is not None:
                value = default
            if validator:
                try:
                    value = validator(value)
                except Exception as e:
                    print(f"Invalid input: {e}")
                    continue
            return value

    print(f"Configuring server '{server_name}'")
    host = get_input("Enter host", default="127.0.0.1")
    port = get_input("Enter port", default="8000", validator=lambda v: int(v) if 0 < int(v) < 65536 else (_ for _ in ()).throw(ValueError("Port must be 1-65535")))
    debug = get_input("Enable debug mode? (y/n)", default="n", validator=lambda v: v.lower() in ("y", "n") or (_ for _ in ()).throw(ValueError("Enter 'y' or 'n'")))
    debug = debug.lower() == "y"

    config = {
        "server_name": server_name,
        "host": host,
        "port": port,
        "debug": debug,
    }

    config_path = os.path.join(server_dir, "config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    print(f"Configuration written to {config_path}")
    return config