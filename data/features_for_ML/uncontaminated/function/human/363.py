from mne.io import BaseRaw as MNERaw

def has_montage(raw: MNERaw) -> bool:
    """Check if raw data has channel positions.

    Args:
        raw: MNE Raw object

    Returns:
        True if positions exist
    """
    # Check for digitization points (modern way)
    if raw.info.get("dig"):
        return True
    # Fallback: check if channels have positions
    try:
        montage = raw.get_montage()
        return montage is not None
    except (AttributeError, RuntimeError):
        return False