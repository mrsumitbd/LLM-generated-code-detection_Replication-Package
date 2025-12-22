def get_filepath_owners(codeowners: CodeOwners, filepath: str) -> set[str]:
    owners = set()
    
    for pattern, pattern_owners in codeowners.items():
        if matches_pattern(pattern, filepath):
            owners.update(pattern_owners)
    
    return owners


def matches_pattern(pattern: str, filepath: str) -> bool:
    import fnmatch
    
    # Normalize paths for comparison
    pattern = pattern.lstrip('/')
    filepath = filepath.lstrip('/')
    
    # Handle exact matches
    if pattern == filepath:
        return True
    
    # Handle directory patterns (e.g., "docs/" matches "docs/file.txt")
    if pattern.endswith('/'):
        return filepath.startswith(pattern)
    
    # Handle wildcard patterns
    if fnmatch.fnmatch(filepath, pattern):
        return True
    
    # Handle directory wildcard patterns (e.g., "docs/*" matches "docs/file.txt")
    if fnmatch.fnmatch(filepath, pattern + '/*'):
        return True
    
    return False