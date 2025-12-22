import os

def process_manifest(temp_dir, server_name, pack_file, base_dir, script_dir):
    """Processes the manifest.json file within an extracted .mcpack.

    Args:
        temp_dir (str): Path to the temporary directory.
        server_name (str): The name of the server.
        pack_file (str): Original path to the .mcpack file (for logging).
        base_dir (str): Base directory.
        script_dir (str): Script directory.
    Returns:
        int: 0 on success, error code on failure.
    """
    action = "process manifest"
    if not temp_dir:
        msg_error("process_manifest: temp_dir is empty.")
        return handle_error(2, action)
    if not server_name:
        msg_error("process_manifest: server_name is empty.")
        return handle_error(25, action)
    if not pack_file:
        msg_error("process_manifest: pack_file is empty.")
        return handle_error(2, action)
    manifest_info = extract_manifest_info(temp_dir)
    if manifest_info is None:
        msg_error(
            f"Failed to process {os.path.basename(pack_file)} due to missing or invalid manifest.json"
        )
        return 1

    pack_type, uuid, version, addon_name_from_manifest, formatted_addon_name = (
        manifest_info
    )

    return install_pack(
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
    )