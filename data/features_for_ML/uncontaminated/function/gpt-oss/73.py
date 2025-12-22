def update_list():
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        return
    nums = list(map(int, data))
    updated = [x + 1 for x in nums]
    print(' '.join(map(str, updated)))