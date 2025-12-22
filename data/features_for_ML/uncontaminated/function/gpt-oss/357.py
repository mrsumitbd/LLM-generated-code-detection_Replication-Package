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

    # Pydantic v2 uses `model_fields` and `model_fields_set`
    fields = getattr(self, "model_fields", getattr(self, "__fields__", {}))
    fields_set = getattr(self, "model_fields_set", getattr(self, "__fields_set__", set()))

    for field_name, field_info in fields.items():
        # Skip if the field was not set during initialization
        if field_name not in fields_set:
            continue

        # Check if the field allows None
        allow_none = getattr(field_info, "allow_none", False)
        if not allow_none:
            continue

        # Get the actual value
        value = getattr(self, field_name, None)
        if value is None:
            alias = getattr(field_info, "alias", field_name)
            data[alias] = None

    return data