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
    # Dump all fields using aliases
    raw = self.model_dump(by_alias=True)

    # Map alias names back to field names
    alias_to_name = {f.alias: f.name for f in self.__fields__.values()}

    result: Dict[str, Any] = {}
    for alias, value in raw.items():
        if value is None:
            field_name = alias_to_name.get(alias)
            if field_name is None:
                continue
            field = self.__fields__[field_name]
            # Include None only if the field is nullable and was set at init
            if field_name in self.__fields_set__ and field.allow_none:
                result[alias] = None
            # otherwise skip
        else:
            result[alias] = value

    return result