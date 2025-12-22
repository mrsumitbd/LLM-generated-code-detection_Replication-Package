from typing import Any

def process_item(item: Any, idx: int | None = None) -> str | float:  # noqa: ANN401
    """
    Process an item and optionally use an index.

    - If the item is numeric (int or float), return it as a float.
      If an index is provided, multiply the numeric value by the index.
    - If the item is a string, return it unchanged.
      If an index is provided, prepend the index followed by a colon.
    - For any other type, return its string representation.
    """
    # Handle numeric types
    if isinstance(item, (int, float)):
        value = float(item)
        if idx is not None:
            return value * idx
        return value

    # Handle string types
    if isinstance(item, str):
        if idx is not None:
            return f"{idx}: {item}"
        return item

    # Fallback for other types
    return str(item)