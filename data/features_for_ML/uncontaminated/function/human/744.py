from typing import TYPE_CHECKING, Any, Type, Union, Generic, TypeVar, Callable, Optional, cast

def _validate_non_model_type(*, type_: type[_T], value: object) -> _T:
        model = _create_pydantic_model(type_).validate(value)
        return cast(_T, model.__root__)