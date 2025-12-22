from typing import List, Optional

def _bm_to_str(bms: Optional[List]) -> str:
    """
    Convert a list of bitmask values (or a single value) into a human‑readable string.
    - If `bms` is None, an empty string is returned.
    - If `bms` is a single int or str, it is returned as a string.
    - If `bms` is a list, each element is converted to a hex string if it is an int,
      otherwise its normal string representation is used. Elements are joined by
      " | ".
    """
    if bms is None:
        return ""

    # Handle a single value that is not a list
    if not isinstance(bms, list):
        return str(bms)

    parts = []
    for item in bms:
        if isinstance(item, int):
            parts.append(f"0x{item:X}")
        else:
            parts.append(str(item))
    return " | ".join(parts)