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
    try:
        if pack_type == "data":
            install_dir = os.path.join(base_dir, server_name, "behavior_packs", formatted_addon_name)
        else:
            install_dir = os.path.join(base_dir, server_name, "resource_packs", formatted_addon_name)

        if os.path.exists(install_dir):
            shutil.rmtree(install_dir)

        os.makedirs(install_dir)

        manifest_path = os.path.join(install_dir, "manifest.json")
        with open(manifest_path, "w") as f:
            manifest = {
                "format_version": 2,
                "header": {
                    "name": addon_name_from_manifest,
                    "description": "",
                    "uuid": uuid,
                    "version": version
                },
                "modules": [
                    {
                        "type": pack_type,
                        "uuid": uuid,
                        "version": version
                    }
                ]
            }
            json.dump(manifest, f, indent=4)

        if pack_type == "data":
            shutil.copytree(os.path.join(temp_dir, "behavior_pack"), install_dir)
        else:
            shutil.copytree(os.path.join(temp_dir, "resource_pack"), install_dir)

        logging.info(f"Installed {pack_type} pack: {formatted_addon_name}")
        return 0
    except Exception as e:
        logging.error(f"Error installing {pack_type} pack: {formatted_addon_name}")
        logging.error(e)
        return 1