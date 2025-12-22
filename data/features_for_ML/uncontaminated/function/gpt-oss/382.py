from typing import Any, Dict, get_origin, get_args, Union

def to_dict(self) -> Dict[str, Any]:
    """
    Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    """
    # Base dict using alias
    data: Dict[str, Any] = self.model_dump(by_alias=True)

    # Determine which fields were set at initialization
    fields_set = getattr(self, "__fields_set__", set())

    # Iterate over all fields defined in the model
    for field_name, field in getattr(self, "__fields__", {}).items():
        alias = field.alias
        value = getattr(self, field_name)

        # Skip if value is not None
        if value is not None:
            continue

        # Determine if the field is nullable
        annotation = field.annotation
        origin = get_origin(annotation)
        args = get_args(annotation)

        is_nullable = (
            origin is Union and type(None) in args
        ) or getattr(field, "allow_none", False)

        # If the field is nullable and was set during initialization,
        # keep the None value; otherwise, remove it from the output.
        if not (is_nullable and field_name in fields_set):
            data.pop(alias, None)

    return data