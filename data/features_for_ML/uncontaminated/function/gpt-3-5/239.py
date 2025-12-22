def _central_state_from_ip(n: int, ip: list[list[int]]) -> list[int]:
    k = len(set(sum(ip, [])))
    ans = [0] * n
    for i, piece in enumerate(ip):
        for p in piece:
            ans[p-1] = i
    return ans