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
    # Get the full dump with aliases
    dump = self.model_dump(by_alias=True)

    # Mapping from alias to field name for quick lookup
    alias_to_name = {field.alias: name for name, field in self.model_fields.items()}

    # Fields that were explicitly set during initialization
    fields_set = getattr(self, "__fields_set__", set())

    result: Dict[str, Any] = {}
    for alias, value in dump.items():
        field_name = alias_to_name.get(alias)
        if field_name is None:
            # Should not happen, but skip just in case
            continue

        field_obj = self.model_fields[field_name]

        if value is None:
            # Include None only if the field allows None and was set
            if field_obj.allow_none and field_name in fields_set:
                result[alias] = None
            # otherwise skip
            continue

        # Non-None values are always included
        result[alias] = value

    return result