def sanitize_path(path: str) -> str:
    path = path.replace('\\', '/')
    path = '/'.join(part for part in path.split('/') if part and part != '.')
    parts = []
    for part in path.split('/'):
        if part == '..':
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return '/'.join(parts)