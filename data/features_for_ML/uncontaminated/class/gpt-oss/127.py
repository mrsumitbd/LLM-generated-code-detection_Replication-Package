from __future__ import annotations

import typing
from dataclasses import dataclass
from typing import Any, get_args, get_origin, Union

# Simple Field representation used by the converter
@dataclass
class Field:
    type: Any
    default: Any = None
    has_default: bool = False
    # Optional metadata for complex types
    element_type: Any | None = None
    key_type: Any | None = None
    value_type: Any | None = None
    options: Any | None = None

class TypeConverter:
    """Converts Python type hints to Field objects"""

    @staticmethod
    def convert_type_hint(type_hint: Any, default_value: Any = None, has_default: bool = False) -> Field | None:
        """
        Public entry point for converting a type hint to a Field.
        Handles errors gracefully and returns None if conversion fails.
        """
        try:
            return TypeConverter._convert_type_hint_unsafe(type_hint, default_value, has_default)
        except Exception:
            return None

    @staticmethod
    def _convert_type_hint_unsafe(type_hint: Any, default_value: Any = None, has_default: bool = False) -> Field:
        """
        Low‑level conversion that assumes the type hint is supported.
        Raises TypeError for unsupported hints.
        """
        origin = get_origin(type_hint)
        args = get_args(type_hint)

        # Handle NoneType
        if type_hint is type(None):
            return Field(type=type(None), default=default_value, has_default=has_default)

        # Handle built‑in types
        if origin is None:
            if isinstance(type_hint, type):
                return Field(type=type_hint, default=default_value, has_default=has_default)
            raise TypeError(f"Unsupported type hint: {type_hint}")

        # Handle Union (including Optional)
        if origin is Union:
            # Optional[T] is Union[T, NoneType]
            non_none_args = [arg for arg in args if arg is not type(None)]
            if len(non_none_args) == 1:
                inner = non_none_args[0]
                return TypeConverter._convert_type_hint_unsafe(inner, default_value, has_default)
            # General Union
            return Field(
                type=Union,
                default=default_value,
                has_default=has_default,
                options=args,
            )

        # Handle List[T]
        if origin in (list, typing.List):
            if len(args) != 1:
                raise TypeError(f"List type hint must have one argument: {type_hint}")
            element = TypeConverter._convert_type_hint_unsafe(args[0])
            return Field(
                type=list,
                default=default_value,
                has_default=has_default,
                element_type=element,
            )

        # Handle Dict[K, V]
        if origin in (dict, typing.Dict):
            if len(args) != 2:
                raise TypeError(f"Dict type hint must have two arguments: {type_hint}")
            key = TypeConverter._convert_type_hint_unsafe(args[0])
            value = TypeConverter._convert_type_hint_unsafe(args[1])
            return Field(
                type=dict,
                default=default_value,
                has_default=has_default,
                key_type=key,
                value_type=value,
            )

        # Handle Tuple[T, ...]
        if origin in (tuple, typing.Tuple):
            if len(args) == 2 and args[1] is Ellipsis:
                element = TypeConverter._convert_type_hint_unsafe(args[0])
                return Field(
                    type=tuple,
                    default=default_value,
                    has_default=has_default,
                    element_type=element,
                )
            # Fixed length tuple
            elements = [TypeConverter._convert_type_hint_unsafe(arg) for arg in args]
            return Field(
                type=tuple,
                default=default_value,
                has_default=has_default,
                options=tuple(elements),
            )

        # Handle Set[T]
        if origin in (set, typing.Set):
            if len(args) != 1:
                raise TypeError(f"Set type hint must have one argument: {type_hint}")
            element = TypeConverter._convert_type_hint_unsafe(args[0])
            return Field(
                type=set,
                default=default_value,
                has_default=has_default,
                element_type=element,
            )

        # Handle FrozenSet[T]
        if origin in (frozenset, typing.FrozenSet):
            if len(args) != 1:
                raise TypeError(f"FrozenSet type hint must have one argument: {type_hint}")
            element = TypeConverter._convert_type_hint_unsafe(args[0])
            return Field(
                type=frozenset,
                default=default_value,
                has_default=has_default,
                element_type=element,
            )

        # Handle Callable
        if origin in (typing.Callable, typing.Callable):
            return Field(
                type=typing.Callable,
                default=default_value,
                has_default=has_default,
                options=args,
            )

        # If we reach here, the type hint is not supported
        raise TypeError(f"Unsupported type hint: {type_hint}")