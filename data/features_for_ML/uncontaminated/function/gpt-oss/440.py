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
    # Dump the model using aliases
    data: Dict[str, Any] = self.model_dump(by_alias=True)

    # Get the mapping of field names to field definitions
    # Pydantic v1 uses `__fields__`, v2 uses `model_fields`
    fields = getattr(self, "__fields__", getattr(self, "model_fields", {}))
    # Set of fields that were explicitly set during initialization
    fields_set = getattr(self, "__fields_set__", set())

    for field_name, field_def in fields.items():
        # The key used in the output dict is the alias
        alias = getattr(field_def, "alias", field_name)
        if alias not in data:
            continue

        value = data[alias]
        if value is None:
            # Keep None only if the field is nullable and was set at init
            allow_none = getattr(field_def, "allow_none", False)
            if not (allow_none and field_name in fields_set):
                data.pop(alias)

    return data