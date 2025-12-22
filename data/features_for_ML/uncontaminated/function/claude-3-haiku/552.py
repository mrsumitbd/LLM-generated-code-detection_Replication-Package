import os
import json
import shutil
import logging

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
    try:
        manifest_path = os.path.join(temp_dir, "manifest.json")
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        pack_name = manifest["header"]["name"]
        pack_version = manifest["header"]["version"]

        logging.info(f"Processing pack: {pack_name} v{pack_version}")
        logging.info(f"Original pack file: {pack_file}")

        pack_dir = os.path.join(base_dir, f"{pack_name}_{pack_version}")
        if os.path.exists(pack_dir):
            logging.warning(f"Pack directory already exists: {pack_dir}")
            return 1

        os.makedirs(pack_dir)
        shutil.move(temp_dir, pack_dir)

        scripts_dir = os.path.join(pack_dir, "scripts")
        if os.path.exists(scripts_dir):
            shutil.move(scripts_dir, script_dir)
            logging.info(f"Moved scripts to: {script_dir}")

        logging.info(f"Processed pack: {pack_name} v{pack_version}")
        return 0
    except Exception as e:
        logging.error(f"Error processing manifest: {e}")
        return 1