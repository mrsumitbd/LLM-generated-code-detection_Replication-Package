from typing import Dict, Any

def to_dict(self) -> Dict[str, Any]:
    """
    Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    """
    # Use Pydantic's dict method to get alias-based keys.
    # `exclude_unset=True` ensures we only get fields that were set.
    # `exclude_none=False` keeps None values so we can filter them manually.
    raw = self.dict(by_alias=True, exclude_unset=True, exclude_none=False)

    # Build a mapping from alias to field name for quick lookup.
    alias_to_name = {field.alias: name for name, field in self.__fields__.items()}

    result: Dict[str, Any] = {}
    for alias, value in raw.items():
        field_name = alias_to_name.get(alias, alias)
        # Include None only if the field was explicitly set during init.
        if value is None and field_name not in self.__fields_set__:
            continue
        result[alias] = value

    return result