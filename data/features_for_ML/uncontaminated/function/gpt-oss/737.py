from typing import Any, Dict, get_origin, get_args, Union

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
    # Base dict: use model_dump with alias and exclude None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Determine the fields mapping (Pydantic v1 vs v2)
    fields_map = getattr(self, "__fields__", getattr(self, "model_fields", {}))

    # Helper to check if a field is nullable
    def is_nullable(field) -> bool:
        # Pydantic v2: field.allow_none
        if hasattr(field, "allow_none"):
            return field.allow_none
        # Fallback: check annotation for Optional
        ann = getattr(field, "annotation", None)
        if ann is None:
            return False
        origin = get_origin(ann)
        if origin is Union:
            return type(None) in get_args(ann)
        return False

    # Add nullable fields that were explicitly set to None
    for field_name, field in fields_map.items():
        if field_name in getattr(self, "__fields_set__", set()):
            value = getattr(self, field_name, None)
            if value is None and is_nullable(field):
                alias = getattr(field, "alias", field_name)
                data[alias] = None

    # Merge additional properties
    additional = getattr(self, "additional_properties", {})
    if isinstance(additional, dict):
        data.update(additional)

    return data