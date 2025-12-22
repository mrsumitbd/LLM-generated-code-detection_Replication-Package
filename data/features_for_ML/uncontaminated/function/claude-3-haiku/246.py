def _split_newline(line: str) -> tuple[str, str]:
    parts = line.split('\n', maxsplit=1)
    if len(parts) == 1:
        return parts[0], ''
    else:
        return parts[0], parts[1]