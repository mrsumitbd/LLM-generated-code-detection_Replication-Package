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
    # Base dict without None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Determine which fields were set at initialization
    set_fields = getattr(self, "__fields_set__", set())

    # Iterate over all fields to add nullable ones that were set
    for field_name, field in getattr(self, "__fields__", {}).items():
        # Skip if not set
        if field_name not in set_fields:
            continue

        # Determine if the field is nullable
        # Pydantic v1: field.allow_none
        # Pydantic v2: field.allow_none
        is_nullable = getattr(field, "allow_none", False)

        # If the field is nullable and its value is None, add it
        if is_nullable:
            alias = getattr(field, "alias", field_name)
            # Only add if not already present (i.e., value was None)
            if alias not in data:
                data[alias] = None

    return data