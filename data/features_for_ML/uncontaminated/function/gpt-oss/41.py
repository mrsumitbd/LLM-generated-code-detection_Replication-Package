import sys

def generate_path(duration, mask):
    """
    Generate a Hamiltonian path on a 2^duration x 2^duration grid that
    starts at (0, 0) and ends at (size-1, size-1), avoiding cells
    marked in the bitmask `mask`.  The mask is an integer where bit i
    corresponds to the cell at row = i // size, col = i % size.
    The function returns a string of directions ('U', 'D', 'L', 'R')
    representing the path, or None if no path exists.
    """
    sys.setrecursionlimit(1000000)

    size = 1 << duration
    total_cells = size * size

    # Build set of blocked cells from mask
    blocked = set()
    m = mask
    idx = 0
    while m:
        if m & 1:
            r = idx // size
            c = idx % size
            blocked.add((r, c))
        m >>= 1
        idx += 1

    # If start or end is blocked, no path
    if (0, 0) in blocked or (size - 1, size - 1) in blocked:
        return None

    visited = [[False] * size for _ in range(size)]
    visited[0][0] = True
    target_cells = total_cells - len(blocked)

    dirs = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    solution = None
    path = []

    def dfs(r, c, steps):
        nonlocal solution
        if solution is not None:
            return
        if steps == target_cells:
            if (r, c) == (size - 1, size - 1):
                solution = ''.join(path)
            return

        # Generate possible moves with heuristic (Warnsdorff's rule)
        moves = []
        for dr, dc, d in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and not visited[nr][nc] and (nr, nc) not in blocked:
                # Count onward moves
                count = 0
                for dr2, dc2, _ in dirs:
                    nr2, nc2 = nr + dr2, nc + dc2
                    if 0 <= nr2 < size and 0 <= nc2 < size and not visited[nr2][nc2] and (nr2, nc2) not in blocked:
                        count += 1
                moves.append((count, nr, nc, d))
        moves.sort(key=lambda x: x[0])

        for _, nr, nc, d in moves:
            visited[nr][nc] = True
            path.append(d)
            dfs(nr, nc, steps + 1)
            path.pop()
            visited[nr][nc] = False
            if solution is not None:
                return

    dfs(0, 0, 1)
    return solution