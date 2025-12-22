from pydantic import ValidationError

def _get_validation_error(msg: str, loc: str) -> ValidationError:
    return ValidationError([
        {
            "loc": (loc,),
            "msg": msg,
            "type": "value_error"
        }
    ])