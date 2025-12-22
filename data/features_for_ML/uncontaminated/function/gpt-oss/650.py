import os
import pathlib
import re

def sanitize_path(path: str) -> str:
    """
    Sanitize a filesystem path to prevent directory traversal and other
    potentially dangerous patterns.

    The function performs the following steps:
    1. Removes any null bytes.
    2. Normalizes the path using os.path.normpath.
    3. Strips any leading slashes or drive letters to make the path relative.
    4. Removes any leading '..' components that could escape the intended
       directory.
    5. Ensures the resulting path does not contain any remaining '..' segments.
    6. Returns the sanitized path as a string.

    Parameters
    ----------
    path : str
        The input path to sanitize.

    Returns
    -------
    str
        A sanitized, relative path safe for use within a controlled directory.
    """
    # 1. Remove null bytes
    path = path.replace('\0', '')

    # 2. Normalize path
    path = os.path.normpath(path)

    # 3. Make path relative: strip leading slashes or drive letters
    # On Windows, remove drive letter if present
    if os.name == 'nt':
        # Remove drive letter (e.g., C:\)
        path = re.sub(r'^[a-zA-Z]:[\\/]', '', path)
    # Remove leading slashes
    path = path.lstrip('/\\')

    # 4. Remove leading '..' components
    parts = pathlib.PurePath(path).parts
    safe_parts = []
    for part in parts:
        if part == '..':
            # Skip to avoid escaping
            continue
        safe_parts.append(part)

    # 5. Reconstruct path
    sanitized = os.path.join(*safe_parts) if safe_parts else ''

    # 6. Ensure no '..' remains
    if '..' in pathlib.PurePath(sanitized).parts:
        sanitized = sanitized.replace('..', '')

    return sanitized