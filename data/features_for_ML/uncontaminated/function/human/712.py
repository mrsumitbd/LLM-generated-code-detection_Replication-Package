from colorama import Fore, Style, init
import glob
import os

def install_worlds(server_name, base_dir, script_dir):
    """Provides a menu to select and install .mcworld files.

    Args:
        server_name (str): The name of the server.
        base_dir (str): The base directory where servers are stored.
        script_dir (str): The directory where the script is located.
    Returns:
        int: 0 on success, error code on failure.

    """
    action = "install worlds"

    if not server_name:
        msg_error("install_worlds: server_name is empty.")
        return handle_error(25, action)

    content_dir = os.path.join(script_dir, "content", "worlds")
    server_dir = os.path.join(base_dir, server_name)

    if not os.path.isdir(content_dir):
        msg_warn(f"Content directory not found: {content_dir}.  No worlds to install.")
        return 0

    world_name = get_world_name(server_name, base_dir)
    if world_name is None:
        msg_error("Failed to get world name from server.properties.")
        return handle_error(11, action)
    if not world_name:
        msg_error("Could not find level-name in server.properties")
        return handle_error(11, action)
    msg_debug(f"World name from server.properties: {world_name}")

    # Use glob to find .mcworld files.
    mcworld_files = glob.glob(os.path.join(content_dir, "*.mcworld"))

    if not mcworld_files:
        msg_warn(f"No .mcworld files found in {content_dir}")
        return 0

    # Create a list of base file names.
    file_names = [os.path.basename(file) for file in mcworld_files]

    # Display the menu and get user selection
    print(Fore.CYAN + "Available worlds to install:" + Style.RESET_ALL)
    for i, file_name in enumerate(file_names):
        print(f"{i + 1}. {file_name}")

    while True:
        try:
            choice = int(input(f"Select a world to install (1-{len(file_names)}): "))
            if 1 <= choice <= len(file_names):
                selected_file = mcworld_files[choice - 1]
                break  # Valid choice
            else:
                msg_warn("Invalid selection. Please choose a valid option.")
        except ValueError:
            msg_warn("Invalid input. Please enter a number.")

    # Confirm deletion of existing world.
    msg_warn("Installing a new world will DELETE the existing world!")
    while True:
        confirm_choice = input("Are you sure you want to proceed? (y/n): ").lower()
        if confirm_choice in ("yes", "y"):
            break
        elif confirm_choice in ("no", "n"):
            msg_warn("World installation canceled.")
            return 0
        else:
            msg_warn("Invalid input. Please answer 'yes' or 'no'.")

    return extract_world(server_name, selected_file, base_dir)