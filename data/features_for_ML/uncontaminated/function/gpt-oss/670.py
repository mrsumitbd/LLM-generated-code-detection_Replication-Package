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
    # Start with a dump that excludes all None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Add back None for nullable fields that were explicitly set
    for field_name in getattr(self, "__fields_set__", set()):
        field_info = self.__fields__.get(field_name)
        if field_info is None:
            continue
        # In Pydantic v1/v2, `allow_none` indicates a nullable field
        if getattr(field_info, "allow_none", False):
            alias = field_info.alias
            # Only add if the value is actually None
            if getattr(self, field_name, None) is None:
                data[alias] = None

    return data