def sanitize_path(path: str) -> str:
    parts = path.split('/')
    sanitized_parts = []
    for part in parts:
        if part == '..':
            if sanitized_parts:
                sanitized_parts.pop()
        elif part and part != '.':
            sanitized_parts.append(part)
    return '/' + '/'.join(sanitized_parts)