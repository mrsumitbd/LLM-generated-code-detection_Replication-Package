def _get_parameter_descriptions(
    dataclass_type: Type, parent_field: Optional[str] = None, **kwargs
) -> List[ParameterDescription]:
    """Get the descriptions of the parameters in the dataclass with nested field
    support.

    Args:
        dataclass_type: The dataclass type to get descriptions for
        parent_field: Name of the parent field if this is a nested parameter
        **kwargs: Additional keyword arguments

    Returns:
        List of ParameterDescription objects describing all fields including nested ones
    """
    from dataclasses import fields, is_dataclass
    from typing import get_origin, get_args
    
    descriptions = []
    
    if not is_dataclass(dataclass_type):
        return descriptions
    
    for field in fields(dataclass_type):
        field_type = field.type
        
        # Handle Optional and Union types
        origin = get_origin(field_type)
        args = get_args(field_type)
        
        # Unwrap Optional (Union[X, None])
        if origin is Union:
            non_none_args = [arg for arg in args if arg is not type(None)]
            if non_none_args:
                field_type = non_none_args[0]
        
        # Build the full parameter name
        if parent_field:
            param_name = f"{parent_field}.{field.name}"
        else:
            param_name = field.name
        
        # Check if the field type is a dataclass (nested)
        if is_dataclass(field_type):
            # Recursively get descriptions for nested dataclass
            nested_descriptions = _get_parameter_descriptions(
                field_type, parent_field=param_name, **kwargs
            )
            descriptions.extend(nested_descriptions)
        else:
            # Create a ParameterDescription for this field
            description = ParameterDescription(
                name=param_name,
                description=field.metadata.get("description", "") if field.metadata else "",
                type=field_type,
                required=field.default is MISSING and field.default_factory is MISSING,
                default=field.default if field.default is not MISSING else None,
            )
            descriptions.append(description)
    
    return descriptions