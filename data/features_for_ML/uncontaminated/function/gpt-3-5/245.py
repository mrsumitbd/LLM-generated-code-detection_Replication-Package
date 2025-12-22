def _get_colored_text(text: str, color: str) -> str:
    return f"\033[38;2;{color}m{text}\033[0m"