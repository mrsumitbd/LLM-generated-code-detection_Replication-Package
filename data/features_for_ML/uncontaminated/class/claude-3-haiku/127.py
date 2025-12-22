from typing import Any, Union, Optional, Tuple, Type

class TypeConverter:
    """Converts Python type hints to Field objects"""

    @staticmethod
    def convert_type_hint(type_hint: Type[Any], default_value: Any = None, has_default: bool = False) -> Tuple[Type[Any], Any, bool]:
        try:
            return TypeConverter._convert_type_hint_unsafe(type_hint, default_value, has_default)
        except ValueError:
            raise ValueError(f"Invalid type hint: {type_hint}")

    @staticmethod
    def _convert_type_hint_unsafe(type_hint: Type[Any], default_value: Any = None, has_default: bool = False) -> Tuple[Type[Any], Any, bool]:
        if type_hint is Any:
            return type_hint, default_value, has_default
        elif type_hint is Union[None, ...]:
            return type(None), default_value, has_default
        elif hasattr(type_hint, "__origin__") and type_hint.__origin__ is Union:
            types = type_hint.__args__
            if len(types) == 2 and type(None) in types:
                return next(t for t in types if t is not type(None)), default_value, has_default
            else:
                raise ValueError(f"Invalid Union type hint: {type_hint}")
        else:
            return type_hint, default_value, has_default