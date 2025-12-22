import re
import re
from typing import Any, Dict, List, Optional, Tuple, Union
import re

def _pick_webmerc(candidates: List[str]) -> Optional[str]:
        if not candidates:
            return None
        # Prefer explicit EPSG:3857 first
        for pref in candidates:
            if "3857" in pref:
                return pref
        # Then other common aliases
        import re

        alias_pattern = r"900913|google|mercator"
        for pref in candidates:
            if re.search(alias_pattern, pref, flags=re.IGNORECASE):
                return pref
        return candidates[0]