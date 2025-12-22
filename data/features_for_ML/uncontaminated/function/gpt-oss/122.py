from typing import Any, Iterator

def _recurse(node: Any) -> Iterator[Any]:
    """
    Recursively traverse a nested structure (dict, list, tuple, set) and yield all leaf values.
    """
    if isinstance(node, dict):
        for value in node.values():
            yield from _recurse(value)
    elif isinstance(node, (list, tuple, set)):
        for item in node:
            yield from _recurse(item)
    else:
        yield node