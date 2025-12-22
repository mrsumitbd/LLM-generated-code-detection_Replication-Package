from typing import List, Optional
from urllib.parse import urlparse

def _pick_webmerc(candidates: List[str]) -> Optional[str]:
    """
    Return the first candidate that appears to refer to a "webmerc" resource.
    A candidate is considered a match if its hostname or path contains the
    substring "webmerc" (case‑insensitive). If no candidate matches, return None.
    """
    for cand in candidates:
        # Try to parse as URL; if it fails, treat the whole string as a path
        try:
            parsed = urlparse(cand)
            host = parsed.hostname or ""
            path = parsed.path or ""
        except Exception:
            host = ""
            path = cand

        if "webmerc" in host.lower() or "webmerc" in path.lower():
            return cand
    return None