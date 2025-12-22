from typing import Any, Dict

def to_dict(self) -> Dict[str, Any]:
    """
    Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    * Fields in `self.additional_properties` are added to the output dict.
    """
    # Dump the model excluding unset fields and excluding None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_unset=True, exclude_none=True)

    # Add nullable fields that were explicitly set to None
    for field_name in getattr(self, "__fields_set__", set()):
        field = getattr(self, "__fields__", {}).get(field_name)
        if field is None:
            continue
        # In Pydantic v2, `allow_none` indicates the field accepts None
        if getattr(field, "allow_none", False):
            value = getattr(self, field_name, None)
            if value is None:
                alias = getattr(field, "alias", field_name)
                data[alias] = None

    # Merge any additional properties
    additional = getattr(self, "additional_properties", None)
    if isinstance(additional, dict):
        data.update(additional)

    return data