def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
    if not last_values:
        return start
    else:
        return last_values[-1] + 1