def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
    """
    Apply consistent spacing around assignment operators.

    Args:
        line: The line to format
        use_spaces: Whether to use spaces around operators

    Returns:
        The formatted line
    """
    operators = ['=', '+=', '-=', '*=', '/=', '//=', '%=', '**=', '&=', '|=', '^=', '>>=', '<<=']
    formatted_line = ''
    in_string = False
    for char in line:
        if char in ['"', "'"]:
            in_string = not in_string
        if char in operators and not in_string:
            if use_spaces:
                formatted_line += f' {char} '
            else:
                formatted_line += char
        else:
            formatted_line += char
    return formatted_line.strip()