def cal_identity_based_on_MDtag(MDtag: List[Tuple[str, str]]) -> float:
    """Approximate alignment identity based on MD tag (ignoring indels).
    Fix deletion length: consecutive letters after '^' represent deletion length."""
    total_matches = 0
    total_length = 0
    for match, op in MDtag:
        if op.isdigit():
            total_length += int(op)
            total_matches += int(op)
        elif op.startswith('^'):
            total_length += len(op) - 1
        else:
            total_length += len(match)
    return total_matches / total_length