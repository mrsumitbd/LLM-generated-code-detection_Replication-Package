def ensure_parent_directory_exists(abs_path: Path) -> None:
    """Ensure parent directory of the given path exists, creating it if necessary.

    Args:
        abs_path (str): Absolute path to the directory.

    Raises:
        OSError: If the directory cannot be created.

    """
    parent_dir = abs_path.parent
    if not parent_dir.exists():
        try:
            parent_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create parent directory: {parent_dir}") from e