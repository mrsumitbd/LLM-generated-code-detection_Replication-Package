def _looks_like_path(name: str) -> bool:
    return any(char in name for char in ['/', '\\', '.'])