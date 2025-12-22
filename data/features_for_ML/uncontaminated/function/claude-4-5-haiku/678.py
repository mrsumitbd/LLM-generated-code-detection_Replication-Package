def rules_dir_writable() -> bool:
    """
    Checks if Prometheus rules directory is writable
    """
    import os
    import tempfile
    
    # Common Prometheus rules directory paths
    possible_paths = [
        "/etc/prometheus/rules",
        "/etc/prometheus",
        "/prometheus/rules",
        "/var/lib/prometheus/rules",
        os.path.expanduser("~/.prometheus/rules"),
    ]
    
    # Try to find and check the rules directory
    for path in possible_paths:
        if os.path.isdir(path):
            if os.access(path, os.W_OK):
                return True
    
    # If no standard path found, try to create a test file in a common location
    for path in possible_paths:
        if os.path.exists(path):
            try:
                test_file = os.path.join(path, ".write_test")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                return True
            except (IOError, OSError):
                continue
    
    return False