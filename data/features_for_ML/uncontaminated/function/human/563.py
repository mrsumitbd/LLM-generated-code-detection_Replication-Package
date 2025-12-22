from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

def _chunk_string(value: str, size: int) -> List[str]:
    if size <= 0:
        size = 65536
    return [value[i : i + size] for i in range(0, len(value), size)]