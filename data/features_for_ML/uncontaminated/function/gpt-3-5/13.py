def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
    if use_spaces:
        return line.replace('=', ' = ')
    else:
        return line.replace(' = ', '=')