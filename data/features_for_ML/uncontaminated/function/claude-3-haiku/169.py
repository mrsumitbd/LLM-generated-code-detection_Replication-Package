def get_file_content(
    filepath: Path
) -> Dict[str, str]:
    """
    Get content of a file.
    Args:
        filepath: Path to a file
    Returns:
        A string containing file content
    Raises:
        IOError: if read content of `filepath` failed
    """
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return {'content': content}
    except IOError as e:
        raise IOError(f"Failed to read content of '{filepath}': {e}")