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
    out: Dict[str, Any] = {}

    # Iterate over all defined fields
    for field_name, field_info in self.__fields__.items():
        # Resolve the alias (use field name if alias is None)
        key = field_info.alias or field_name

        # Get the current value
        value = getattr(self, field_name)

        # Determine if the field was set during initialization
        was_set = field_name in getattr(self, "__fields_set__", set())

        # Include None only if the field is nullable and was set
        if value is None:
            if was_set and getattr(field_info, "allow_none", False):
                out[key] = None
            # otherwise skip
            continue

        # For non-None values, always include
        out[key] = value

    # Add any additional properties
    additional = getattr(self, "additional_properties", {})
    if isinstance(additional, dict):
        out.update(additional)

    return out