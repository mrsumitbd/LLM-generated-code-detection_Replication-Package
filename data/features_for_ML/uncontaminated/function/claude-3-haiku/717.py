def _strip_properly_formatted_commas(expr: str):
    result = ""
    in_string = False
    in_tuple = False
    for char in expr:
        if char == "'":
            in_string = not in_string
        elif char == "(":
            in_tuple = True
        elif char == ")":
            in_tuple = False
        elif char == "," and not in_string and not in_tuple:
            continue
        else:
            result += char
    return result