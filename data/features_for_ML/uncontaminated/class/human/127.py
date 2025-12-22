import gc
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)
import inspect
from types import UnionType
import gc
import gc
import gc
import gc

class TypeConverter:
    """Converts Python type hints to Field objects"""

    @staticmethod
    def convert_type_hint(type_hint, default_value=None, has_default=False):
        """Convert a type hint to a Field object"""

        # Protect against GC issues during type processing
        gc.disable()
        try:
            return TypeConverter._convert_type_hint_unsafe(
                type_hint, default_value, has_default
            )
        finally:
            gc.enable()

    @staticmethod
    def _convert_type_hint_unsafe(type_hint, default_value=None, has_default=False):
        """Convert a type hint to a Field object (internal method without GC protection)"""

        # Determine if field is optional based on type annotation only
        # A field is optional if it's explicitly typed as Optional[Type] or Union[Type, None]
        # Having a default value does NOT make a field optional - it just provides a fallback
        is_optional = False

        # Handle Union types (e.g., str | None, Union[str, None])
        origin = get_origin(type_hint)
        if origin is Union or (UnionType and origin is UnionType):
            args = get_args(type_hint)

            # Check if it's Optional (Union with None)
            if len(args) == 2 and type(None) in args:
                # Optional type
                non_none_type = args[0] if args[1] is type(None) else args[1]
                field = TypeConverter._convert_type_hint_unsafe(
                    non_none_type, default_value, has_default
                )
                field.optional = True  # Optional fields are always optional
                return field
            else:
                # TODO: Handle other Union types
                raise NotImplementedError(f"Union types not yet supported: {type_hint}")

        # Create FastAPI-style Field with auto-detected type
        field_default = default_value if has_default else ...
        field = Field(default=field_default)
        field._field_type = type_hint
        field.optional = is_optional or has_default

        # Check if this is a nested BaseModel
        if (
            inspect.isclass(type_hint)
            and issubclass(type_hint, BaseModel)
            and type_hint is not BaseModel
        ):
            field._is_nested_model = True
            field._nested_model_class = type_hint
        else:
            field._is_nested_model = False
            field._nested_model_class = None

        # Check if this is a List[BaseModel] pattern
        field._is_list_of_models = False
        field._list_item_model_class = None
        if hasattr(type_hint, "__origin__") and type_hint.__origin__ is list:
            args = get_args(type_hint)
            if args and len(args) == 1:
                item_type = args[0]
                if (
                    inspect.isclass(item_type)
                    and issubclass(item_type, BaseModel)
                    and item_type is not BaseModel
                ):
                    field._is_list_of_models = True
                    field._list_item_model_class = item_type

        return field