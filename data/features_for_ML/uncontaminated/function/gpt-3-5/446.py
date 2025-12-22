from pathlib import Path

def ensure_parent_directory_exists(abs_path: Path) -> None:
    parent_dir = abs_path.parent
    if not parent_dir.exists():
        parent_dir.mkdir(parents=True, exist_ok=True)