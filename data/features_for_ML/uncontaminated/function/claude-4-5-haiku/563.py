def _chunk_string(value: str, size: int) -> list[str]:
    return [value[i:i+size] for i in range(0, len(value), size)]