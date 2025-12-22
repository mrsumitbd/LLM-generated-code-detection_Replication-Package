def has_montage(raw: MNERaw) -> bool:
    """Check if raw data has channel positions.

    Args:
        raw: MNE Raw object

    Returns:
        True if positions exist
    """
    return raw.get_montage() is not None