from typing import List, Optional

def _pick_webmerc(candidates: List[str]) -> Optional[str]:
    for candidate in candidates:
        if candidate.startswith('webmerc'):
            return candidate
    return None