def _central_state_from_ip(n: int, ip: list[list[int]]) -> list[int]:
    """Given list of lists of identical pieces, generates central state.

    Pieces in `ip` are 1-indexed.
    Returns array `ans` of length n such that ans[i]=ans[j] if and only if pieces i and j are identical.
    Values in this array are integers from 0 to k-1 where k is number of colors.
    It is allowed to not specify singleton groups of equivalent pieces.
    """
    ans = list(range(n))
    color = 0
    
    for group in ip:
        if group:
            # Assign the same color to all pieces in this group
            for piece in group:
                ans[piece - 1] = color  # Convert from 1-indexed to 0-indexed
            color += 1
    
    return ans