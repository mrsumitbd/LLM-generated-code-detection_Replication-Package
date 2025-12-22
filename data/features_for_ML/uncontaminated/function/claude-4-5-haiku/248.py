def _get_validation_error(msg: str, loc: str) -> ValidationError:
    from pydantic import ValidationError, PydanticErrorMixin
    from pydantic_core import PydanticCustomError
    
    error = PydanticCustomError('value_error', msg)
    return ValidationError.from_exception_data(
        title='ValueError',
        line_errors=[{
            'type': 'value_error',
            'loc': (loc,),
            'msg': msg,
            'input': None,
        }]
    )