def process_item(item: Any, idx: int | None = None) -> str | float:  # noqa: ANN401
    if isinstance(item, str):
        return f"Processed string: {item}"
    elif isinstance(item, (int, float)):
        if idx is not None:
            return item * idx
        else:
            return item
    else:
        return "Invalid input type"