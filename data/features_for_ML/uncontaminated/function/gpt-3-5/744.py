def _validate_non_model_type(*, type_: type[_T], value: object) -> _T:
    if not isinstance(value, type_):
        raise TypeError(f"Expected value of type {type_.__name__}, but received value of type {type(value).__name__}")
    return value