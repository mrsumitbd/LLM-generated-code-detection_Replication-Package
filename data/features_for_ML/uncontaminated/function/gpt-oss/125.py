from typing import Any, Dict

def to_dict(self) -> Dict[str, Any]:
    """
    Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    """
    # Start with a dict that excludes None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Determine which fields were explicitly set during initialization
    set_fields = getattr(self, "__fields_set__", set())

    for field_name, field in self.__fields__.items():
        # Skip if the field was not set or its value is not None
        if field_name not in set_fields or getattr(self, field_name) is not None:
            continue

        # Check if the field is nullable
        # In Pydantic v1: field.allow_none
        # In Pydantic v2: field.annotation may contain None
        is_nullable = getattr(field, "allow_none", False)
        if not is_nullable:
            # Try to infer from the annotation if allow_none is not present
            try:
                from typing import get_origin, get_args, Union
                ann = field.annotation
                if get_origin(ann) is Union and type(None) in get_args(ann):
                    is_nullable = True
            except Exception:
                pass

        if is_nullable:
            alias = field.alias
            data[alias] = None

    return data