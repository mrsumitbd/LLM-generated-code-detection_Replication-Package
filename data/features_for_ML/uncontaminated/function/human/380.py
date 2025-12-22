def rounded_corners(corner_string):
    if corner_string == "all":
        return True, True, True, True

    corners = corner_string.split(",")
    corner_map = {
        "top_left": 0,
        "top_right": 1,
        "bottom_right": 2,
        "bottom_left": 3
    }
    result = [False] * 4
    for corner in corners:
        corner = corner.strip()
        if corner in corner_map:
            result[corner_map[corner]] = True

    return tuple(result)