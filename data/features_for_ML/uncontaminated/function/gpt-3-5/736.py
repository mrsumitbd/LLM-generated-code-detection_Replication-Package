def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
    if name == 'increment':
        return start + count
    elif name == 'decrement':
        return start - count
    elif name == 'double':
        return start * 2
    elif name == 'triple':
        return start * 3
    elif name == 'last':
        return last_values[-1]
    else:
        return None