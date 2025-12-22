def rounded_corners(corner_string):
    corners = corner_string.split()
    result = []
    for corner in corners:
        if corner.endswith('px'):
            value = int(corner[:-2])
            result.append(f"{value}px")
        else:
            result.append(corner)
    return ' '.join(result)