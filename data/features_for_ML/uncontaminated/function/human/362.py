import shutil
import os

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
    """Installs a pack based on its type (data/resources).

    Args:
        type (str): "data" or "resources".
        temp_dir (str): Path to the temporary directory.
        server_name (str): The name of the server.
        pack_file (str): Original path to the .mcpack file (for logging).
        base_dir (str): The base directory for servers.
        script_dir (str): The script directory
        uuid (str): The UUID from the manifest.
        version (list): The version array from the manifest.
        addon_name_from_manifest (str): The addon name from the manifest.
        formatted_addon_name (str): The formatted addon name.
    Returns:
        int: 0 on success, error code on failure.
    """
    action = "install pack"
    if not pack_type:
        msg_error("install_pack: type is empty.")
        return handle_error(2, action)
    if not temp_dir:
        msg_error("install_pack: temp_dir is empty.")
        return handle_error(2, action)
    if not server_name:
        msg_error("install_pack: server_name is empty.")
        return handle_error(25, action)
    if not pack_file:
        msg_error("install_pack: pack_file is empty.")
        return handle_error(2, action)

    world_name = get_world_name(server_name, base_dir)
    if not world_name:
        msg_error("Could not find level-name in server.properties")
        return handle_error(11, action)

    behavior_dir = os.path.join(
        base_dir, server_name, "worlds", world_name, "behavior_packs"
    )
    resource_dir = os.path.join(
        base_dir, server_name, "worlds", world_name, "resource_packs"
    )
    behavior_json = os.path.join(
        base_dir, server_name, "worlds", world_name, "world_behavior_packs.json"
    )
    resource_json = os.path.join(
        base_dir, server_name, "worlds", world_name, "world_resource_packs.json"
    )

    # Create directories if they don't exist
    os.makedirs(behavior_dir, exist_ok=True)
    os.makedirs(resource_dir, exist_ok=True)

    if pack_type == "data":
        msg_info(f"Installing behavior pack to {server_name}")
        addon_behavior_dir = os.path.join(
            behavior_dir, f"{formatted_addon_name}_{'.'.join(map(str, version))}"
        )
        os.makedirs(addon_behavior_dir, exist_ok=True)
        try:
            # Copy all files from temp_dir to addon_behavior_dir
            for item in os.listdir(temp_dir):
                s = os.path.join(temp_dir, item)
                d = os.path.join(addon_behavior_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)  # Copy files

            update_pack_json(behavior_json, uuid, version)
            msg_ok(f"Installed {os.path.basename(pack_file)} to {server_name}.")
            return 0
        except OSError as e:
            msg_error(f"Failed to copy behavior pack files: {e}")
            return handle_error(1, action)

    elif pack_type == "resources":
        msg_info(f"Installing resource pack to {server_name}")
        addon_resource_dir = os.path.join(
            resource_dir, f"{formatted_addon_name}_{'.'.join(map(str, version))}"
        )
        os.makedirs(addon_resource_dir, exist_ok=True)
        try:
            # Copy all files from temp_dir to addon_resource_dir
            for item in os.listdir(temp_dir):
                s = os.path.join(temp_dir, item)
                d = os.path.join(addon_resource_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)  # Copy Files
            update_pack_json(resource_json, uuid, version)
            msg_ok(f"Installed {os.path.basename(pack_file)} to {server_name}.")
            return 0
        except OSError as e:
            msg_error(f"Failed to copy resource pack files: {e}")
            return handle_error(1, action)
    else:
        msg_error(f"Unknown pack type: {pack_type}")
        return handle_error(27, action)