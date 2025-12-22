def _central_state_from_ip(n: int, ip: list[list[int]]) -> list[int]:
    """Given list of lists of identical pieces, generates central state.

    Pieces in `ip` are 1-indexed.
    Returns array `ans` of length n such that ans[i]=ans[j] if and only if pieces i and j are identical.
    Values in this array are integers from 0 to k-1 where k is number of colors.
    It is allowed to not specify singleton groups of equivalent pieces.
    """
    ans = [-1] * n
    color = 0
    for group in ip:
        for piece in group:
            ans[piece - 1] = color
        color += 1
    for i in range(n):
        if ans[i] == -1:
            ans[i] = color
            color += 1
    return ans