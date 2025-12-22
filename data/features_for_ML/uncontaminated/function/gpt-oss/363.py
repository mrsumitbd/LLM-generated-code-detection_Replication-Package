import numpy as np

def has_montage(raw: "MNERaw") -> bool:
    """Check if raw data has channel positions.

    Args:
        raw: MNE Raw object

    Returns:
        True if positions exist
    """
    # MNE stores channel location info in raw.info['chs'][i]['loc']
    # The first three entries of 'loc' are the 3‑D position.
    # If any channel has a non‑zero position, we consider a montage present.
    chs = raw.info.get("chs", [])
    for ch in chs:
        loc = ch.get("loc")
        if loc is None:
            continue
        # loc is a 7‑element array: [x, y, z, ...]
        if not np.allclose(loc[0:3], 0):
            return True
    return False