def to_dict(self) -> Dict[str, Any]:
    """Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    """
    data = {}
    for field in self.__fields__.values():
        value = getattr(self, field.alias, None)
        if value is not None or field.allow_none and field.name in self.__dict__:
            data[field.alias] = value
    return data