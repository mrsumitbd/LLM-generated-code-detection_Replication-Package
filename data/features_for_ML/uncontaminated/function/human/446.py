from pathlib import Path

def ensure_parent_directory_exists(abs_path: Path) -> None:
    """Ensure parent directory of the given path exists, creating it if necessary.

    Args:
        abs_path (str): Absolute path to the directory.

    Raises:
        OSError: If the directory cannot be created.

    """
    directory = abs_path.parent
    if directory and not directory.exists():
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            msg = f"Failed to create directory '{directory}': {e!s}"
            raise OSError(msg) from e