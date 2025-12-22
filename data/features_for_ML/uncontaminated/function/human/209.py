from colorama import Fore, Style, init
import re
import os

def configure_server_properties(server_name, base_dir):
    """Configures common server properties interactively.

    Args:
        server_name (str): The name of the server.
        base_dir (str): The base directory where servers are stored.
    """
    server_dir = os.path.join(base_dir, server_name)
    action = "configure server properties"
    msg_info(f"Configuring server properties for '{server_name}'")

    if not server_name:
        msg_error("configure_server_properties: server_name is empty.")
        return handle_error(25, action)

    server_properties = os.path.join(server_dir, "server.properties")
    if not os.path.exists(server_properties):
        msg_error("server.properties not found!")
        return handle_error(11, action)
    # Default values
    DEFAULT_PORT = "19132"
    DEFAULT_IPV6_PORT = "19133"

    # Read existing properties
    current_properties = {}
    try:
        with open(server_properties, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:  # Ensure line is not empty and has "="
                    key, value = line.split("=", 1)  # Split only on the first "="
                    current_properties[key] = value
    except OSError as e:
        msg_error(f"Failed to read server.properties {e}")
        return handle_error(14, action)  # Failed to configure server properties

    # Prompts with validation and defaults
    input_server_name = input(
        Fore.CYAN
        + f"Enter server name [Default: {current_properties.get('server-name', '')}]: "
        + Style.RESET_ALL
    )
    input_server_name = input_server_name or current_properties.get("server-name", "")
    while ";" in input_server_name:
        msg_error("Server name cannot contain semicolons.")
        input_server_name = input(
            Fore.CYAN
            + f"Enter server name [Default: {current_properties.get('server-name', '')}]: "
            + Style.RESET_ALL
        )
        input_server_name = input_server_name or current_properties.get(
            "server-name", ""
        )

    input_level_name = input(
        Fore.CYAN
        + f"Enter level name [Default: {current_properties.get('level-name', '')}]: "
        + Style.RESET_ALL
    )
    input_level_name = input_level_name or current_properties.get("level-name", "")
    input_level_name = input_level_name.replace(" ", "_")
    while not re.match(r"^[a-zA-Z0-9_-]+$", input_level_name):
        msg_error(
            "Invalid level-name. Only alphanumeric characters, hyphens, and underscores are allowed (spaces converted to underscores)."
        )
        input_level_name = input(
            Fore.CYAN
            + f"Enter level name [Default: {current_properties.get('level-name', '')}]: "
            + Style.RESET_ALL
        )
        input_level_name = input_level_name or current_properties.get("level-name", "")
        input_level_name = input_level_name.replace(" ", "_")

    input_gamemode = select_option(
        "Select gamemode:",
        current_properties.get("gamemode", "survival"),
        "survival",
        "creative",
        "adventure",
    )
    input_difficulty = select_option(
        "Select difficulty:",
        current_properties.get("difficulty", "easy"),
        "peaceful",
        "easy",
        "normal",
        "hard",
    )
    input_allow_cheats = select_option(
        "Allow cheats:",
        current_properties.get("allow-cheats", "false"),
        "true",
        "false",
    )

    while True:
        input_port = input(
            Fore.CYAN
            + f"Enter IPV4 Port [Default: {current_properties.get('server-port', DEFAULT_PORT)}]: "
            + Style.RESET_ALL
        )
        input_port = input_port or current_properties.get("server-port", DEFAULT_PORT)
        if re.match(r"^[0-9]+$", input_port) and 1024 <= int(input_port) <= 65535:
            break
        msg_error("Invalid port number. Please enter a number between 1024 and 65535.")

    while True:
        input_port_v6 = input(
            Fore.CYAN
            + f"Enter IPV6 Port [Default: {current_properties.get('server-portv6', DEFAULT_IPV6_PORT)}]: "
            + Style.RESET_ALL
        )
        input_port_v6 = input_port_v6 or current_properties.get(
            "server-portv6", DEFAULT_IPV6_PORT
        )
        if re.match(r"^[0-9]+$", input_port_v6) and 1024 <= int(input_port_v6) <= 65535:
            break
        msg_error(
            "Invalid IPV6 port number. Please enter a number between 1024 and 65535."
        )

    input_lan_visibility = select_option(
        "Enable LAN visibility:",
        current_properties.get("enable-lan-visibility", "true"),
        "true",
        "false",
    )
    input_allow_list = select_option(
        "Enable allow list:",
        current_properties.get("allow-list", "false"),
        "true",
        "false",
    )

    while True:
        input_max_players = input(
            Fore.CYAN
            + f"Enter max players [Default: {current_properties.get('max-players', '10')}]: "
            + Style.RESET_ALL
        )
        input_max_players = input_max_players or current_properties.get(
            "max-players", "10"
        )
        if re.match(r"^[0-9]+$", input_max_players):
            break
        msg_error("Invalid number for max players.")

    input_permission_level = select_option(
        "Select default permission level:",
        current_properties.get("default-player-permission-level", "member"),
        "visitor",
        "member",
        "operator",
    )

    while True:
        input_render_distance = input(
            Fore.CYAN
            + f"Default render distance [Default: {current_properties.get('view-distance', '10')}]: "
            + Style.RESET_ALL
        )
        input_render_distance = input_render_distance or current_properties.get(
            "view-distance", "10"
        )
        if (
            re.match(r"^[0-9]+$", input_render_distance)
            and int(input_render_distance) >= 5
        ):
            break
        msg_error(
            "Invalid render distance. Please enter a number greater than or equal to 5."
        )

    while True:
        input_tick_distance = input(
            Fore.CYAN
            + f"Default tick distance [Default: {current_properties.get('tick-distance', '4')}]: "
            + Style.RESET_ALL
        )
        input_tick_distance = input_tick_distance or current_properties.get(
            "tick-distance", "4"
        )
        if (
            re.match(r"^[0-9]+$", input_tick_distance)
            and 4 <= int(input_tick_distance) <= 12
        ):
            break
        msg_error("Invalid tick distance. Please enter a number between 4 and 12.")
    input_level_seed = input(
        Fore.CYAN + f"Enter level seed: " + Style.RESET_ALL
    )  # No default or validation
    input_online_mode = select_option(
        "Enable online mode:",
        current_properties.get("online-mode", "true"),
        "true",
        "false",
    )
    input_texturepack_required = select_option(
        "Require texture pack:",
        current_properties.get("texturepack-required", "false"),
        "true",
        "false",
    )

    # Update properties
    modify_server_properties(server_properties, "server-name", input_server_name)
    modify_server_properties(server_properties, "level-name", input_level_name)
    modify_server_properties(server_properties, "gamemode", input_gamemode)
    modify_server_properties(server_properties, "difficulty", input_difficulty)
    modify_server_properties(server_properties, "allow-cheats", input_allow_cheats)
    modify_server_properties(server_properties, "server-port", input_port)
    modify_server_properties(server_properties, "server-portv6", input_port_v6)
    modify_server_properties(
        server_properties, "enable-lan-visibility", input_lan_visibility
    )
    modify_server_properties(server_properties, "allow-list", input_allow_list)
    modify_server_properties(server_properties, "max-players", input_max_players)
    modify_server_properties(
        server_properties, "default-player-permission-level", input_permission_level
    )
    modify_server_properties(server_properties, "view-distance", input_render_distance)
    modify_server_properties(server_properties, "tick-distance", input_tick_distance)
    modify_server_properties(server_properties, "level-seed", input_level_seed)
    modify_server_properties(server_properties, "online-mode", input_online_mode)
    modify_server_properties(
        server_properties, "texturepack-required", input_texturepack_required
    )

    msg_ok("Server properties configured")
    return 0