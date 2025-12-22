def rounded_corners(corner_string):
    top = "╭" + "─" * (len(corner_string) + 2) + "╮\n"
    middle = "│ " + corner_string + " │\n"
    bottom = "╰" + "─" * (len(corner_string) + 2) + "╯\n"
    return top + middle + bottom