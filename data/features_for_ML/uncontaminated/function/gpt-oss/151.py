def format_file_size(bytes_size):
    """
    Convert a file size in bytes to a human‑readable string using powers of 1024.

    Parameters
    ----------
    bytes_size : int | float
        The size in bytes.

    Returns
    -------
    str
        Human‑readable representation, e.g. "512 B", "1.0 KB", "2.3 MB", etc.
    """
    if bytes_size < 0:
        raise ValueError("bytes_size must be non‑negative")

    # For sizes less than 1 KiB, just return bytes
    if bytes_size < 1024:
        return f"{int(bytes_size)} B"

    # Define units
    units = ["KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(bytes_size) / 1024.0

    for unit in units:
        if size < 1024:
            # Use one decimal place; strip trailing .0 if integer
            formatted = f"{size:.1f}".rstrip("0").rstrip(".")
            return f"{formatted} {unit}"
        size /= 1024.0

    # If size is larger than EB, just return the value in EB
    formatted = f"{size:.1f}".rstrip("0").rstrip(".")
    return f"{formatted} EB"