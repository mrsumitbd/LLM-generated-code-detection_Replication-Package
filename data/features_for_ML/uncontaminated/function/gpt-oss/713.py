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
    # Use Pydantic's built‑in dump to get the alias‑based dict
    data = self.model_dump(by_alias=True)

    # Determine the set of fields that were explicitly set at init
    if hasattr(self, "model_fields_set"):  # Pydantic v2
        set_fields = self.model_fields_set
    else:  # Pydantic v1
        set_fields = getattr(self, "__fields_set__", set())

    # Iterate over all fields defined on the model
    for field_name, field in self.model_fields.items():
        alias = field.alias
        # Skip if the alias is not present in the dumped data
        if alias not in data:
            continue

        value = data[alias]
        if value is None:
            # Keep None only if the field allows None and was set at init
            allow_none = getattr(field, "allow_none", False)
            if not (allow_none and field_name in set_fields):
                # Remove the key from the output
                del data[alias]

    return data