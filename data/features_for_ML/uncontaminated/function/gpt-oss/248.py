from typing import Any
try:
    # pydantic v1
    from pydantic import ValidationError as PydanticValidationError
except ImportError:
    # pydantic v2
    from pydantic import ValidationError as PydanticValidationError

def _get_validation_error(msg: str, loc: str) -> PydanticValidationError:
    """
    Create a ValidationError instance with the given message and location.

    Parameters
    ----------
    msg : str
        The error message.
    loc : str
        The location of the error (e.g., field name).

    Returns
    -------
    ValidationError
        A ValidationError instance containing the supplied message and location.
    """
    # Build the error structure expected by pydantic
    error = {
        "loc": (loc,),
        "msg": msg,
        "type": "value_error",
    }

    # In pydantic v1 the constructor expects (errors, model)
    # In pydantic v2 it expects (errors, model)
    # We pass None for the model as we don't have a specific model context.
    return PydanticValidationError(errors=[error], model=None)