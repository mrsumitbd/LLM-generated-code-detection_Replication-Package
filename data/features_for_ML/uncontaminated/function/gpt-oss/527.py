from __future__ import annotations

from dataclasses import is_dataclass, fields, MISSING
from typing import Any, List, Optional, Type, get_origin, get_args

# Assume ParameterDescription is defined elsewhere in the same package.
# Import it here. If it is not available, this import will fail and the
# function will not be usable. Adjust the import path as necessary.
try:
    from .parameter_description import ParameterDescription
except Exception:  # pragma: no cover
    # Fallback stub for type checking / documentation purposes.
    class ParameterDescription:
        def __init__(self, name: str, type: Any, default: Any = None, description: str = ""):
            self.name = name
            self.type = type
            self.default = default
            self.description = description

        def __repr__(self):
            return (
                f"ParameterDescription(name={self.name!r}, type={self.type!r}, "
                f"default={self.default!r}, description={self.description!r})"
            )


def _get_parameter_descriptions(
    dataclass_type: Type,
    parent_field: Optional[str] = None,
    **kwargs,
) -> List[ParameterDescription]:
    """
    Get the descriptions of the parameters in the dataclass with nested field
    support.

    Args:
        dataclass_type: The dataclass type to get descriptions for
        parent_field: Name of the parent field if this is a nested parameter
        **kwargs: Additional keyword arguments

    Returns:
        List of ParameterDescription objects describing all fields including nested ones
    """
    if not is_dataclass(dataclass_type):
        raise TypeError(f"{dataclass_type!r} is not a dataclass")

    descriptions: List[ParameterDescription] = []

    for f in fields(dataclass_type):
        # Build the full field name, including parent prefix if any
        full_name = f"{parent_field}.{f.name}" if parent_field else f.name

        # Resolve the actual type, handling typing.Optional and other generics
        field_type = f.type
        origin = get_origin(field_type)
        args = get_args(field_type)

        # If the field is a generic Optional[T] or Union[..., None], unwrap it
        if origin is Union and type(None) in args:
            # Keep the original type for description purposes
            pass

        # Determine default value
        if f.default is not MISSING:
            default_value = f.default
        elif f.default_factory is not MISSING:  # type: ignore[attr-defined]
            default_value = f.default_factory()  # type: ignore[call-arg]
        else:
            default_value = None

        # Extract description from metadata if present
        description_text = f.metadata.get("description", "") if f.metadata else ""

        # Check if the field type itself is a dataclass (nested)
        # Handle typing generics that may wrap a dataclass (e.g., List[MyDataclass])
        nested_dataclass_type = None
        if is_dataclass(field_type):
            nested_dataclass_type = field_type
        elif origin in (list, List, tuple, Tuple, set, Set, frozenset, FrozenSet):
            # For container types, check if the contained type is a dataclass
            if args and is_dataclass(args[0]):
                nested_dataclass_type = args[0]
        elif origin is Union:
            # For Union types, check each argument
            for arg in args:
                if is_dataclass(arg):
                    nested_dataclass_type = arg
                    break

        if nested_dataclass_type:
            # Recursively get nested descriptions
            nested_descs = _get_parameter_descriptions(
                nested_dataclass_type, parent_field=full_name, **kwargs
            )
            descriptions.extend(nested_descs)
        else:
            # Create a ParameterDescription for this field
            param_desc = ParameterDescription(
                name=full_name,
                type=field_type,
                default=default_value,
                description=description_text,
            )
            descriptions.append(param_desc)

    return descriptions