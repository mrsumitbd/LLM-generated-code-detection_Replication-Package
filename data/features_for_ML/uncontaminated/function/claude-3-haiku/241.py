import hashlib
import pathlib

def _warn_if_mismatch(old: pathlib.Path, new: pathlib.Path, *, key: str) -> bool:
    try:
        with open(old, 'rb') as f:
            old_hash = hashlib.sha256(f.read()).hexdigest()
        with open(new, 'rb') as f:
            new_hash = hashlib.sha256(f.read()).hexdigest()
    except (IOError, OSError):
        return False

    if old_hash != new_hash:
        print(f"Warning: {key} hash mismatch between {old} and {new}")
        return True
    return False