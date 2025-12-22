def _get_parameter_descriptions(dataclass_type: Type, parent_field: Optional[str] = None, **kwargs) -> List[ParameterDescription]:
    parameter_descriptions = []
    for field_name, field_type in dataclass_type.__dataclass_fields__.items():
        full_field_name = f"{parent_field}.{field_name}" if parent_field else field_name
        if hasattr(field_type.type, "__dataclass_fields__"):
            parameter_descriptions.extend(_get_parameter_descriptions(field_type.type, full_field_name, **kwargs))
        else:
            parameter_descriptions.append(ParameterDescription(name=full_field_name, type=field_type.type, **kwargs))
    return parameter_descriptions