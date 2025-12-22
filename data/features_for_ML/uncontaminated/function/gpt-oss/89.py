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
    # Start with a dict that excludes all None values
    data: Dict[str, Any] = self.model_dump(by_alias=True, exclude_none=True)

    # Determine which fields were explicitly set at initialization
    set_fields = getattr(self, "__fields_set__", set())

    for field_name, field in self.__fields__.items():
        # Skip if the field was not set
        if field_name not in set_fields:
            continue

        value = getattr(self, field_name)
        if value is not None:
            continue  # already included by model_dump

        # Check if the field type allows None
        field_type = field.type_
        nullable = False
        origin = get_origin(field_type)
        if origin is Union:
            if type(None) in get_args(field_type):
                nullable = True
        elif field_type is type(None):
            nullable = True

        if nullable:
            alias = field.alias
            data[alias] = None

    return data