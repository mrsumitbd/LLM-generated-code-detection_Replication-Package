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
    # Base dict: all non‑None values, using aliases
    out: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Determine the set of fields that were explicitly set
    fields_set = getattr(self, "__fields_set__", getattr(self, "model_fields_set", set()))

    # Iterate over all declared fields
    for field_name, field_info in getattr(self, "model_fields", {}).items():
        if field_name not in fields_set:
            continue

        value = getattr(self, field_name, None)

        # Skip if value is not None (already in out)
        if value is not None:
            continue

        # Determine if the field is nullable
        nullable = getattr(field_info, "allow_none", False)
        if not nullable:
            ann = getattr(field_info, "annotation", None)
            if ann is not None:
                origin = get_origin(ann)
                if origin is Union:
                    nullable = type(None) in get_args(ann)

        if nullable:
            alias = getattr(field_info, "alias", field_name)
            out[alias] = None

    # Merge any additional properties
    additional = getattr(self, "additional_properties", {})
    if isinstance(additional, dict):
        out.update(additional)

    return out