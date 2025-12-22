from itertools import (takewhile, repeat, groupby)
from typing import Dict, List, Tuple

def cal_identity_based_on_MDtag(MDtag: List[Tuple[str, str]]) -> float:
    """Approximate alignment identity based on MD tag (ignoring indels).
    Fix deletion length: consecutive letters after '^' represent deletion length."""
    md_val = ""
    for tag, val in MDtag:
        if tag == "MD":
            md_val = val
            break
    if not md_val:
        return -1.0

    groups = [''.join(list(g)) for _, g in groupby(md_val, key=lambda x: x.isdigit())]
    match_base = 0
    mismatch_base = 0
    i = 0
    while i < len(groups):
        token = groups[i]
        if token.isdigit():
            match_base += int(token)
            i += 1
        else:
            # Handle deletion: starts with '^' followed by bases
            if token.startswith("^"):
                mismatch_base += max(len(token) - 1, 0)
            else:
                mismatch_base += len(token)
            i += 1
    denom = match_base + mismatch_base
    if denom <= 0:
        return -1.0
    return float(match_base) / denom