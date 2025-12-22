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
    # Base dict: include only set fields, exclude None values
    data: Dict[str, Any] = self.model_dump(
        by_alias=True,
        exclude_unset=True,
        exclude_none=True,
    )

    # Add nullable fields that were explicitly set to None
    for field_name, field in self.__fields__.items():
        if field_name in self.__fields_set__:
            value = getattr(self, field_name)
            if value is None:
                # In Pydantic v2, `allow_none` indicates if None is allowed
                allow_none = getattr(field, "allow_none", False)
                if allow_none:
                    alias = field.alias
                    data[alias] = None

    # Merge additional properties
    if hasattr(self, "additional_properties"):
        data.update(self.additional_properties)

    return data