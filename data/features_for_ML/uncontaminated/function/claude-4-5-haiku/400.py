def _bm_to_str(bms: Optional[List]):
    if bms is None:
        return ""
    
    result = []
    for bm in bms:
        if isinstance(bm, dict):
            items = []
            for key, value in bm.items():
                items.append(f"{key}={value}")
            result.append("{" + ", ".join(items) + "}")
        else:
            result.append(str(bm))
    
    return ", ".join(result)