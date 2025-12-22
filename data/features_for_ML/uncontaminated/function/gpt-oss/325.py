import os

def _is_c_file(path) -> bool:
    """
    Return True if the given path refers to a C source file.
    The check is based on the file extension and is case‑insensitive.
    """
    _, ext = os.path.splitext(path)
    return ext.lower() == ".c"