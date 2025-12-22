from pathlib import Path

def ensure_parent_directory_exists(abs_path: Path) -> None:
    """Ensure parent directory of the given path exists, creating it if necessary.

    Args:
        abs_path (Path): Absolute path to the directory.

    Raises:
        OSError: If the directory cannot be created.
    """
    parent = abs_path.parent
    # If the parent is the root (e.g., Path('/') or Path('C:\\')), mkdir will be a no-op.
    parent.mkdir(parents=True, exist_ok=True)