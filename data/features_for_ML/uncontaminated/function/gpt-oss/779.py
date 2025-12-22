from typing import List, Tuple

def cal_identity_based_on_MDtag(MDtag: List[Tuple[str, str]]) -> float:
    """
    Approximate alignment identity based on MD tag (ignoring indels).
    MDtag is a list of tuples where the first element is either a numeric
    string indicating a run of matches or a string of mismatched bases.
    The second element (if present) contains deletion information and is ignored.
    """
    matches = 0
    mismatches = 0

    for match_part, _ in MDtag:
        if match_part.isdigit():
            matches += int(match_part)
        else:
            mismatches += len(match_part)

    total = matches + mismatches
    return matches / total if total > 0 else 0.0