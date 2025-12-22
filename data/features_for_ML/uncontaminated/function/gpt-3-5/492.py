from pathlib import Path

def is_valid_db(dir_in: Path) -> bool:
    if not dir_in.is_dir():
        return False
    if not (dir_in / "__init__.py").is_file():
        return False
    if not (dir_in / "py.typed").is_file():
        return False
    return True