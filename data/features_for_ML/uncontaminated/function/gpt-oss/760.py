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
    # Dump only fields that were set during initialization
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_unset=True)

    # Iterate over all fields to filter out non‑nullable None values
    for field_name, field in self.model_fields.items():
        alias = field.alias
        if alias not in data:
            continue

        value = data[alias]
        if value is None:
            # Keep None only if the field is nullable and was set at init
            if not field.allow_none or field_name not in self.__fields_set__:
                del data[alias]

    return data