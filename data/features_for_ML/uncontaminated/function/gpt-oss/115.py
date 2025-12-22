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
    result: Dict[str, Any] = {}
    # Pydantic BaseModel attributes
    fields = getattr(self, "__fields__", {})
    fields_set = getattr(self, "__fields_set__", set())

    def is_nullable(field_info) -> bool:
        # Pydantic v1
        if hasattr(field_info, "allow_none"):
            return field_info.allow_none
        # Pydantic v2: check annotation for Optional
        ann = getattr(field_info, "annotation", None)
        if ann is None:
            return False
        origin = get_origin(ann)
        if origin is Union:
            return type(None) in get_args(ann)
        return False

    for name, field_info in fields.items():
        value = getattr(self, name, None)
        alias = getattr(field_info, "alias", name) or name
        if value is None:
            if name in fields_set and is_nullable(field_info):
                result[alias] = None
            # else skip
        else:
            result[alias] = value

    return result