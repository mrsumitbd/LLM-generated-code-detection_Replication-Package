from typing import Any, Dict, get_args, get_origin, Union, Optional, Type

def to_dict(self) -> Dict[str, Any]:
    """
    Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    """
    # Base dict: include only set fields, exclude None values
    base: Dict[str, Any] = self.model_dump(
        by_alias=True,
        exclude_unset=True,
        exclude_none=True,
    )

    # Helper to determine if a field annotation is nullable
    def _is_nullable(annotation: Any) -> bool:
        # Direct NoneType
        if annotation is type(None):
            return True
        origin = get_origin(annotation)
        if origin is Union:
            return type(None) in get_args(annotation)
        # Optional is just Union[..., None]
        if origin is Optional:
            return True
        return False

    # Add None for nullable fields that were explicitly set
    for field_name in getattr(self, "model_fields_set", set()):
        value = getattr(self, field_name, None)
        if value is None:
            field = self.model_fields[field_name]
            if _is_nullable(field.annotation):
                alias = field.alias
                base[alias] = None

    return base