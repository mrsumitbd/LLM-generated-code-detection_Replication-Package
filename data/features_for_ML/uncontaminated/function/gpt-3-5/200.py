def INPUT_TYPES(s):
    if s.isdigit():
        return "INTEGER"
    elif s.replace(".", "", 1).isdigit():
        return "FLOAT"
    else:
        return "STRING"