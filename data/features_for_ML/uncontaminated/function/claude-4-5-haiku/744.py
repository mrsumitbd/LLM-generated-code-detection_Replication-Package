def _validate_non_model_type(*, type_: type[_T], value: object) -> _T:
    if not isinstance(value, type_):
        raise TypeError(f"Expected {type_.__name__}, got {type(value).__name__}")
    return value