def _bm_to_str(bms: Optional[List]) -> str:
    if bms is None:
        return ""
    return "".join([chr(bm) for bm in bms])