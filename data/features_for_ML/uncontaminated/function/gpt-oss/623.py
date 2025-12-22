from typing import Any, Dict, Union, get_origin, get_args

def to_dict(self) -> Dict[str, Any]:
    """
    Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    """
    # Base dict without None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Helper to determine if a field is nullable
    def _is_nullable(field) -> bool:
        # Pydantic v1
        if hasattr(field, "allow_none"):
            return field.allow_none
        # Pydantic v2: check Optional in annotation
        ann = field.annotation
        origin = get_origin(ann)
        if origin is Union:
            return type(None) in get_args(ann)
        return False

    # Add None for nullable fields that were explicitly set
    for field_name, field in self.__fields__.items():
        if field_name in self.__fields_set__ and _is_nullable(field):
            value = getattr(self, field_name)
            if value is None:
                alias = field.alias
                data[alias] = None

    return data