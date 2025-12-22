import os
import shutil

def configure_server_properties(server_name, base_dir):
    """Configures common server properties interactively.

    Args:
        server_name (str): The name of the server.
        base_dir (str): The base directory where servers are stored.
    """
    server_dir = os.path.join(base_dir, server_name)
    if not os.path.exists(server_dir):
        os.makedirs(server_dir)

    print(f"Configuring server properties for {server_name}")

    # Configure server properties interactively
    server_port = int(input("Enter server port: "))
    server_ip = input("Enter server IP address: ")
    server_log_level = input("Enter server log level: ")

    # Save server properties to a configuration file
    config_file = os.path.join(server_dir, "server.conf")
    with open(config_file, "w") as f:
        f.write(f"server_port={server_port}\n")
        f.write(f"server_ip={server_ip}\n")
        f.write(f"server_log_level={server_log_level}\n")

    print(f"Server properties saved to {config_file}")

    # Create a backup of the server directory
    backup_dir = os.path.join(base_dir, f"{server_name}_backup")
    shutil.copytree(server_dir, backup_dir)
    print(f"Server directory backed up to {backup_dir}")