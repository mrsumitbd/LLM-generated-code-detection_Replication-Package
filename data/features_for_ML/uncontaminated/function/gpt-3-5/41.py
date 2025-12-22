def generate_path(duration, mask):
    path = []
    for i in range(duration):
        if mask & (1 << i):
            path.append('right')
        else:
            path.append('down')
    return path