def _warn_if_mismatch(old: pathlib.Path, new: pathlib.Path, *, key: str) -> bool:
    import warnings
    
    try:
        old_content = old.read_bytes() if old.exists() else None
        new_content = new.read_bytes() if new.exists() else None
        
        if old_content != new_content:
            warnings.warn(
                f"Mismatch in {key}: {old} != {new}",
                UserWarning,
                stacklevel=2
            )
            return True
        return False
    except Exception:
        return False