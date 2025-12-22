def _compute_all_transpositions_cayley_growth(n_str: str) -> list[int]:
    n = int(n_str)
    if n == 0:
        return [1]
    if n == 1:
        return [1, 1]
    
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        dp[i][0] = 0
        for j in range(1, n + 1):
            dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
    
    return [dp[n][k] for k in range(n + 1)]