def _pick_webmerc(candidates: List[str]) -> Optional[str]:
    if not candidates:
        return None

    for candidate in candidates:
        if 'webmerc' in candidate.lower():
            return candidate

    return candidates[0]