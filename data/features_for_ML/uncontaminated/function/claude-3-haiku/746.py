def _compute_all_transpositions_cayley_growth(n_str: str) -> list[int]:
    n = int(n_str)
    result = [0] * (n + 1)
    result[0] = 1
    result[1] = 1

    for i in range(2, n + 1):
        for j in range(1, i + 1):
            result[i] += j * result[i - j]

    return result