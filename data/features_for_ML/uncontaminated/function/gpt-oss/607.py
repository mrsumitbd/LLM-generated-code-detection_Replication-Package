import os

def _looks_like_path(name: str) -> bool:
    """Checks whether the string "looks like" a path on the filesystem.

    This does not check whether the target actually exists, only judge from the
    appearance.

    Returns true if any of the following conditions is true:
    * a path separator is found (either os.path.sep or os.path.altsep);
    * a dot is found (which represents the current directory).
    """
    if not name:
        return False

    sep = os.path.sep
    altsep = os.path.altsep

    for ch in name:
        if ch == sep or (altsep is not None and ch == altsep) or ch == '.':
            return True
    return False