def process_item(item: Any, idx: int | None = None) -> str | float:
    if idx is not None:
        return str(item) + str(idx)
    else:
        return float(item)