def _is_c_file(path) -> bool:
    """Check if a file is a C source file based on its extension."""
    if isinstance(path, str):
        return path.endswith(('.c', '.h'))
    return False