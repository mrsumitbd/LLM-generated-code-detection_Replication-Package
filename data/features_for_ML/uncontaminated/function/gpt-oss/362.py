import os
import shutil
import json
import logging

def install_pack(
    pack_type,
    temp_dir,
    server_name,
    pack_file,
    base_dir,
    script_dir,
    uuid,
    version,
    addon_name_from_manifest,
    formatted_addon_name,
):
    """
    Installs a pack based on its type (data/resources).

    Args:
        pack_type (str): "data" or "resources".
        temp_dir (str): Path to the temporary directory.
        server_name (str): The name of the server.
        pack_file (str): Original path to the .mcpack file (for logging).
        base_dir (str): The base directory for servers.
        script_dir (str): The script directory.
        uuid (str): The UUID from the manifest.
        version (list): The version array from the manifest.
        addon_name_from_manifest (str): The addon name from the manifest.
        formatted_addon_name (str): The formatted addon name.

    Returns:
        int: 0 on success, error code on failure.
    """
    # Basic validation
    if not os.path.isfile(pack_file):
        logging.error(f"Pack file does not exist: {pack_file}")
        return 1

    if pack_type not in ("data", "resources"):
        logging.error(f"Unsupported pack type: {pack_type}")
        return 2

    # Determine destination directory
    dest_dir = os.path.join(base_dir, server_name)
    if pack_type == "data":
        dest_dir = os.path.join(dest_dir, "data")
    else:  # resources
        dest_dir = os.path.join(dest_dir, "resourcepacks")

    try:
        os.makedirs(dest_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create destination directory '{dest_dir}': {e}")
        return 3

    # Destination file name: use formatted_addon_name + .mcpack
    dest_file = os.path.join(dest_dir, f"{formatted_addon_name}.mcpack")

    try:
        shutil.copy2(pack_file, dest_file)
    except Exception as e:
        logging.error(f"Failed to copy pack to '{dest_file}': {e}")
        return 4

    # Optional: run a reload script if present
    reload_script = os.path.join(script_dir, "reload_server.sh")
    if os.path.isfile(reload_script):
        try:
            # Use subprocess to call the script
            import subprocess
            subprocess.run([reload_script, server_name], check=True)
        except Exception as e:
            logging.warning(f"Failed to reload server '{server_name}': {e}")

    logging.info(f"Installed {pack_type} pack '{formatted_addon_name}' to '{dest_dir}'.")
    return 0