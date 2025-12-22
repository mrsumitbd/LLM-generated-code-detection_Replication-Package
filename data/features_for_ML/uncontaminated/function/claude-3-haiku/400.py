def _bm_to_str(bms: Optional[List]):
    if bms is None:
        return ''
    return ', '.join(str(bm) for bm in bms)