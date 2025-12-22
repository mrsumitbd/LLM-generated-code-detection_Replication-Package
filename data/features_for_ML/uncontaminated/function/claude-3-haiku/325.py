def _is_c_file(path) -> bool:
    """
    Checks if the given file path represents a C source file.

    Args:
        path (str): The file path to check.

    Returns:
        bool: True if the file is a C source file, False otherwise.
    """
    if not isinstance(path, str) or not path:
        return False

    return path.endswith('.c')