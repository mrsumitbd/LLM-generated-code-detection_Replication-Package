def update_cargo_toml(file_path: Path, version: str) -> tuple[bool, str, str]:
    """
    Update a Cargo.toml file that has hardcoded version (not using workspace).

    Returns: (changed, old_version, new_version)
    """
    import re
    
    # Read the file
    content = file_path.read_text()
    
    # Find the version line in [package] section
    # Match pattern: version = "x.y.z" or version = 'x.y.z'
    pattern = r'(\[package\].*?)version\s*=\s*["\']([^"\']+)["\']'
    
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return (False, "", "")
    
    old_version = match.group(2)
    
    if old_version == version:
        return (False, old_version, version)
    
    # Replace the version
    new_content = re.sub(
        r'(version\s*=\s*)["\']([^"\']+)["\']',
        rf'\1"{version}"',
        content,
        count=1
    )
    
    # Write back to file
    file_path.write_text(new_content)
    
    return (True, old_version, version)