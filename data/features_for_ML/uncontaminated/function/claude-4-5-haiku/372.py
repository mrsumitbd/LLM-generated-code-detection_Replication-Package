def process_item(item: Any, idx: int | None = None) -> str | float:  # noqa: ANN401
    if isinstance(item, (int, float)):
        return float(item)
    elif isinstance(item, str):
        return item
    elif isinstance(item, bool):
        return str(item)
    elif isinstance(item, (list, tuple)):
        if idx is not None and 0 <= idx < len(item):
            return process_item(item[idx], None)
        return str(item)
    elif isinstance(item, dict):
        if idx is not None and idx in item:
            return process_item(item[idx], None)
        return str(item)
    else:
        return str(item)