def to_dict(self) -> Dict[str, Any]:
    """Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    * Fields in `self.additional_properties` are added to the output dict.
    """
    data = self.model_dump(by_alias=True)
    for field, value in data.items():
        if value is None and field not in self.__fields__:
            del data[field]
    data.update(self.additional_properties)
    return data