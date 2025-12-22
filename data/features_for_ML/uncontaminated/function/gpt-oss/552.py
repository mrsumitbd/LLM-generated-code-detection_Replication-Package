import json
import logging
import os
import shutil
from pathlib import Path

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
    logger = logging.getLogger(__name__)
    manifest_path = Path(temp_dir) / "manifest.json"

    # 1. Check that manifest.json exists
    if not manifest_path.is_file():
        logger.error(f"Missing manifest.json in extracted pack: {temp_dir}")
        return 1

    # 2. Load and validate JSON
    try:
        with manifest_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        logger.error(f"Failed to parse manifest.json: {exc}")
        return 2

    required_keys = {"name", "description", "version", "pack_format"}
    missing = required_keys - data.keys()
    if missing:
        logger.error(f"Manifest missing required keys {missing}")
        return 3

    # 3. Prepare output directory
    output_dir = Path(base_dir) / server_name
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        logger.error(f"Could not create output directory {output_dir}: {exc}")
        return 4

    # 4. Copy all extracted files to the output directory
    try:
        for item in Path(temp_dir).iterdir():
            dest = output_dir / item.name
            if item.is_dir():
                shutil.rmtree(dest, ignore_errors=True)
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
    except Exception as exc:
        logger.error(f"Error copying files to {output_dir}: {exc}")
        return 5

    # 5. Optionally create a script file in script_dir (example placeholder)
    try:
        script_path = Path(script_dir) / f"{server_name}_setup.sh"
        script_path.write_text(f"#!/bin/bash\n# Setup for {server_name}\n")
        script_path.chmod(0o755)
    except Exception as exc:
        logger.warning(f"Could not create script file {script_path}: {exc}")

    logger.info(f"Processed manifest for {server_name} from {pack_file}")
    return 0