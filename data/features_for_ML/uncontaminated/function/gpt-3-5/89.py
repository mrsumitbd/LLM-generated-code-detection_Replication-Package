def to_dict(self) -> Dict[str, Any]:
    output_dict = {}
    for field_name in self.__fields__:
        field = self.__fields__[field_name]
        value = getattr(self, field_name)
        if value is not None or (field.required and field_name in self.__dict__):
            output_dict[field.alias] = value
    return output_dict