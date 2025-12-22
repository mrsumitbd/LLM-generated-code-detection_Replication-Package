def _compute_all_transpositions_cayley_growth(n_str: str) -> list[int]:
    # Growth function is given by Stirling numbers, see https://oeis.org/A094638.
    n = int(n_str)
    return [_stirling(n, n + 1 - k) for k in range(1, n + 1)]