def _pick_webmerc(candidates: List[str]) -> Optional[str]:
    """
    Pick a Web Mercator CRS from a list of candidate CRS strings.
    Returns the first Web Mercator CRS found, or None if not found.
    """
    if not candidates:
        return None
    
    webmerc_identifiers = [
        'EPSG:3857',
        'EPSG:102100',
        'EPSG:102113',
        'EPSG:900913',
        'GOOGLE:900913',
        'webmerc',
        'web_mercator',
        'web mercator',
    ]
    
    for candidate in candidates:
        if candidate is None:
            continue
        candidate_upper = candidate.upper()
        for identifier in webmerc_identifiers:
            if identifier.upper() in candidate_upper:
                return candidate
    
    return None