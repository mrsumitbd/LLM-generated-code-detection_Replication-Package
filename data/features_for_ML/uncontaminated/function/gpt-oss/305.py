from __future__ import annotations
from typing import Any, List, Dict, Set

def compute_source_coverage(
    claims: List[Dict[str, Any]], question_references: List[str]
) -> float:
    """
    Compute the source coverage of the extracted claims.

    Parameters
    ----------
    claims : list[dict[str, Any]]
        A list of claim dictionaries. Each claim may contain a 'source' key
        whose value is either a string or an iterable of strings.
    question_references : list[str]
        A list of reference identifiers that should be covered by the claims.

    Returns
    -------
    float
        The fraction of question references that appear in at least one claim's
        source. The value is in the range [0.0, 1.0]. If `question_references`
        is empty, 0.0 is returned.
    """
    if not question_references:
        return 0.0

    # Normalize question references to a set for fast lookup
    ref_set: Set[str] = set(question_references)

    # Collect all sources referenced by claims
    covered: Set[str] = set()

    for claim in claims:
        src = claim.get("source")
        if src is None:
            continue
        # If the source is a string, treat it as a single reference
        if isinstance(src, str):
            if src in ref_set:
                covered.add(src)
        else:
            # Assume iterable of strings (e.g., list, tuple, set)
            try:
                for s in src:
                    if s in ref_set:
                        covered.add(s)
            except TypeError:
                # If src is not iterable, skip it
                continue

    return len(covered) / len(ref_set)