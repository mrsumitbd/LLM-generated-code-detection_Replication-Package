def _get_validation_error(msg: str, loc: str) -> ValidationError:
    return ValidationError(msg, loc)