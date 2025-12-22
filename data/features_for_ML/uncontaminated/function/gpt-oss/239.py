def _central_state_from_ip(n: int, ip: list[list[int]]) -> list[int]:
    """
    Given list of lists of identical pieces, generates central state.

    Pieces in `ip` are 1-indexed.
    Returns array `ans` of length n such that ans[i] = ans[j] iff pieces i and j are identical.
    Values in this array are integers from 0 to k-1 where k is number of colors.
    It is allowed to not specify singleton groups of equivalent pieces.
    """
    # Initialize answer with -1 (unassigned)
    ans = [-1] * n

    # Assign colors to groups in ip
    for color_id, group in enumerate(ip):
        for piece in group:
            # Convert 1-indexed to 0-indexed
            idx = piece - 1
            if 0 <= idx < n:
                ans[idx] = color_id
            else:
                raise ValueError(f"Piece index {piece} out of bounds for n={n}")

    # Assign unique colors to remaining pieces (singletons)
    next_color = len(ip)
    for i in range(n):
        if ans[i] == -1:
            ans[i] = next_color
            next_color += 1

    return ans