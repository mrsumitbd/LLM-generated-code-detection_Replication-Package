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
    # Dump the model excluding all None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Add back None for nullable fields that were explicitly set
    for field_name in getattr(self, "model_fields_set", set()):
        field = self.model_fields[field_name]
        # In Pydantic v2, `allow_none` indicates that None is a valid value
        if getattr(field, "allow_none", False) and getattr(self, field_name) is None:
            alias = getattr(field, "alias", field_name)
            data[alias] = None

    return data