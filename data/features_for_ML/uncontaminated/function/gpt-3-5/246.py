def _split_newline(line: str) -> tuple[str, str]:
    parts = line.split('\n', 1)
    return parts[0], parts[1] if len(parts) > 1 else ''