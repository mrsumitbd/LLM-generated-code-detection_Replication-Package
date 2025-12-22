def get_line1(id: LineFill) -> Line | NA:
    if id.lines:
        return id.lines[0]
    else:
        return NA