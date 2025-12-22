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
    import json
    import os
    
    manifest_path = os.path.join(temp_dir, 'manifest.json')
    
    # Check if manifest.json exists
    if not os.path.exists(manifest_path):
        print(f"Error: manifest.json not found in {temp_dir}")
        return 1
    
    try:
        # Read and parse manifest.json
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse manifest.json from {pack_file}: {e}")
        return 2
    except IOError as e:
        print(f"Error: Failed to read manifest.json from {pack_file}: {e}")
        return 3
    
    # Validate manifest structure
    if not isinstance(manifest, dict):
        print(f"Error: manifest.json is not a valid JSON object in {pack_file}")
        return 4
    
    # Check for required fields
    required_fields = ['format_version', 'header']
    for field in required_fields:
        if field not in manifest:
            print(f"Error: manifest.json missing required field '{field}' in {pack_file}")
            return 5
    
    # Validate header
    if not isinstance(manifest.get('header'), dict):
        print(f"Error: manifest.json header is not a valid object in {pack_file}")
        return 6
    
    header = manifest['header']
    header_required = ['name', 'description', 'version']
    for field in header_required:
        if field not in header:
            print(f"Error: manifest.json header missing required field '{field}' in {pack_file}")
            return 7
    
    return 0