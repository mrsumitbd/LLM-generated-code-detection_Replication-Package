from typing import Any, Dict, get_origin, get_args, Union

def to_dict(self) -> Dict[str, Any]:
    """
    Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    """
    # Support both Pydantic v1 and v2 field containers
    fields = getattr(self, "__fields__", getattr(self, "model_fields", {}))
    fields_set = getattr(self, "__fields_set__", getattr(self, "model_fields_set", set()))

    result: Dict[str, Any] = {}

    for field_name, field in fields.items():
        # Determine the alias to use
        alias = getattr(field, "alias", field_name)

        # Get the current value of the field
        value = getattr(self, field_name, None)

        # Skip fields that are not set and have no value
        if field_name not in fields_set and value is None:
            continue

        # Determine if the field is nullable
        nullable = False
        # Pydantic v1: use outer_type_
        type_hint = getattr(field, "outer_type_", None)
        if type_hint is None:
            # Pydantic v2: use annotation
            type_hint = getattr(field, "annotation", None)

        if type_hint is not None:
            origin = get_origin(type_hint)
            args = get_args(type_hint)
            if origin is Union and type(None) in args:
                nullable = True
            else:
                # Some fields may explicitly allow None via allow_none
                nullable = getattr(field, "allow_none", False)

        # Include None only if the field is nullable and was set
        if value is None:
            if nullable and field_name in fields_set:
                result[alias] = None
            # otherwise skip
            continue

        # For non-None values, include them directly
        result[alias] = value

    return result