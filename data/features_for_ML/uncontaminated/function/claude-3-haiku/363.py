def has_montage(raw: MNERaw) -> bool:
    """Check if raw data has channel positions.

    Args:
        raw: MNE Raw object

    Returns:
        True if positions exist
    """
    try:
        return raw.info['chs'][0]['loc'] is not None
    except (KeyError, IndexError):
        return False