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
    # Start with a dict that excludes None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Determine which fields were explicitly set during initialization
    fields_set = getattr(self, "__fields_set__", set())

    # Iterate over all fields defined on the model
    for field_name, field in self.__fields__.items():
        # Skip if the field was not set at init
        if field_name not in fields_set:
            continue

        # Determine if the field is nullable
        allow_none = getattr(field, "allow_none", False)
        if not allow_none:
            # In Pydantic v2 the attribute may be missing; fallback to annotation check
            anno = getattr(field, "annotation", None)
            if anno is not None:
                # Check if None is part of a Union
                try:
                    from typing import get_origin, get_args
                    if get_origin(anno) is Union and type(None) in get_args(anno):
                        allow_none = True
                except Exception:
                    pass

        if not allow_none:
            continue

        # If the value is None, include it in the output
        if getattr(self, field_name) is None:
            alias = field.alias
            data[alias] = None

    return data