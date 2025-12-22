import os
import sys
import shutil
import zipfile

def install_worlds(server_name, base_dir, script_dir):
    """Provides a menu to select and install .mcworld files.

    Args:
        server_name (str): The name of the server.
        base_dir (str): The base directory where servers are stored.
        script_dir (str): The directory where the script is located.
    Returns:
        int: 0 on success, error code on failure.
    """
    # Determine server and world directories
    server_dir = os.path.join(base_dir, server_name)
    world_dir = os.path.join(server_dir, "world")

    # Find all .mcworld files in script_dir
    mcworld_files = [f for f in os.listdir(script_dir) if f.lower().endswith(".mcworld")]
    if not mcworld_files:
        print(f"No .mcworld files found in '{script_dir}'.")
        return 1

    # Display menu
    print("Select a world to install:")
    for idx, fname in enumerate(mcworld_files, start=1):
        print(f"  {idx}. {fname}")

    # Prompt for selection
    try:
        choice = int(input(f"Enter number (1-{len(mcworld_files)}): ").strip())
    except ValueError:
        print("Invalid input. Expected a number.")
        return 1

    if not (1 <= choice <= len(mcworld_files)):
        print("Choice out of range.")
        return 1

    selected_file = os.path.join(script_dir, mcworld_files[choice - 1])

    # Ensure server directory exists
    if not os.path.isdir(server_dir):
        try:
            os.makedirs(server_dir, exist_ok=True)
        except OSError as e:
            print(f"Failed to create server directory '{server_dir}': {e}")
            return 1

    # Remove existing world folder if present
    if os.path.isdir(world_dir):
        try:
            shutil.rmtree(world_dir)
        except OSError as e:
            print(f"Failed to remove existing world directory '{world_dir}': {e}")
            return 1

    # Extract the .mcworld file
    try:
        with zipfile.ZipFile(selected_file, 'r') as zf:
            # Extract all contents into server_dir
            zf.extractall(server_dir)
    except (zipfile.BadZipFile, OSError) as e:
        print(f"Failed to extract '{selected_file}': {e}")
        return 1

    # After extraction, the world data is usually in a subfolder named 'world'
    extracted_world = os.path.join(server_dir, "world")
    if not os.path.isdir(extracted_world):
        # Some .mcworld files may contain a different folder name; try to find it
        subdirs = [d for d in os.listdir(server_dir) if os.path.isdir(os.path.join(server_dir, d))]
        if subdirs:
            extracted_world = os.path.join(server_dir, subdirs[0])
        else:
            print("Could not locate extracted world folder.")
            return 1

    # Rename extracted folder to 'world' if it's not already
    if extracted_world != world_dir:
        try:
            os.rename(extracted_world, world_dir)
        except OSError as e:
            print(f"Failed to rename extracted world folder: {e}")
            return 1

    print(f"World '{mcworld_files[choice - 1]}' installed successfully to '{world_dir}'.")
    return 0