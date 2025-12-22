import pathlib

def _warn_if_mismatch(old: pathlib.Path, new: pathlib.Path, *, key: str) -> bool:
    if old == new:
        return False
    _warn_mismatched(old, new, key=key)
    return True