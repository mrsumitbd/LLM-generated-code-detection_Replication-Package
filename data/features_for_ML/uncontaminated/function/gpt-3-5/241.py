def _warn_if_mismatch(old: pathlib.Path, new: pathlib.Path, *, key: str) -> bool:
    if old.stat().st_mtime != new.stat().st_mtime:
        print(f"Warning: Mismatch found for key '{key}'")
        return True
    return False