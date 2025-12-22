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
    # Dump the model with aliases, keeping all fields (including None)
    data = self.model_dump(by_alias=True, exclude_unset=False, exclude_none=False)

    # Determine which fields were set during initialization
    if hasattr(self, "model_fields_set"):  # Pydantic v2
        set_fields = self.model_fields_set
    else:  # Pydantic v1
        set_fields = getattr(self, "__fields_set__", set())

    # Iterate over the model's fields to decide whether to keep None values
    if hasattr(self, "model_fields"):  # Pydantic v2
        fields = self.model_fields.items()
    else:  # Pydantic v1
        fields = self.__fields__.items()

    for field_name, field in fields:
        alias = field.alias
        if alias in data and data[alias] is None:
            # Keep None only if the field is nullable and was set at init
            if not getattr(field, "allow_none", False) or field_name not in set_fields:
                data.pop(alias)

    return data