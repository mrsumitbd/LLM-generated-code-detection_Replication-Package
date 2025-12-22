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
    import os
    import shutil
    from pathlib import Path
    
    try:
        # Validate pack_type
        if pack_type not in ["data", "resources"]:
            return 1
        
        # Construct paths
        server_path = os.path.join(base_dir, server_name)
        
        if pack_type == "data":
            pack_dir = os.path.join(server_path, "datapacks")
        else:  # resources
            pack_dir = os.path.join(server_path, "resourcepacks")
        
        # Create pack directory if it doesn't exist
        os.makedirs(pack_dir, exist_ok=True)
        
        # Find the pack content in temp_dir
        temp_pack_path = None
        for root, dirs, files in os.walk(temp_dir):
            if "manifest.json" in files:
                temp_pack_path = root
                break
        
        if not temp_pack_path:
            return 2
        
        # Create destination directory with formatted name
        dest_path = os.path.join(pack_dir, formatted_addon_name)
        
        # Remove existing pack if it exists
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        
        # Copy the pack to destination
        shutil.copytree(temp_pack_path, dest_path)
        
        return 0
        
    except Exception as e:
        return 3