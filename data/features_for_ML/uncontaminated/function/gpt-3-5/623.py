def to_dict(self) -> Dict[str, Any]:
    output_dict = {}
    for field_name in self.__fields__:
        field = self.__fields__[field_name]
        value = getattr(self, field_name)
        if value is not None or (value is None and field.required):
            output_dict[field.alias] = value
    return output_dict