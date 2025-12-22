from __future__ import annotations

from typing import TypeVar, Type

try:
    # Try to import BaseModel from pydantic if available
    from pydantic import BaseModel
except Exception:
    BaseModel = None  # type: ignore

_T = TypeVar("_T")


def _validate_non_model_type(*, type_: Type[_T], value: object) -> _T:
    """
    Validate that *value* is an instance of *type_* and is not a Pydantic BaseModel.

    Parameters
    ----------
    type_ : type[_T]
        The expected type of *value*.
    value : object
        The value to validate.

    Returns
    -------
    _T
        The validated value, cast to the expected type.

    Raises
    ------
    TypeError
        If *value* is a Pydantic BaseModel instance or not an instance of *type_*.
    """
    # Reject Pydantic BaseModel instances if BaseModel is available
    if BaseModel is not None and isinstance(value, BaseModel):
        raise TypeError(
            f"Value is a Pydantic model instance; expected {type_.__name__}"
        )

    if not isinstance(value, type_):
        raise TypeError(
            f"Expected value of type {type_.__name__} but got {type(value).__name__}"
        )

    return value