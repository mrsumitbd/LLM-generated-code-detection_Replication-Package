def _get_base_model_descriptions(model_cls: "BaseModel") -> List[ParameterDescription]:
    """Extract parameter descriptions from a Pydantic BaseModel class."""
    descriptions = []
    
    # Get the model fields
    if hasattr(model_cls, 'model_fields'):
        # Pydantic v2
        fields = model_cls.model_fields
    elif hasattr(model_cls, '__fields__'):
        # Pydantic v1
        fields = model_cls.__fields__
    else:
        return descriptions
    
    for field_name, field_info in fields.items():
        # Get the field type
        if hasattr(field_info, 'annotation'):
            field_type = field_info.annotation
        else:
            field_type = field_info.type_
        
        # Get the description
        description = None
        if hasattr(field_info, 'description'):
            description = field_info.description
        
        # Get default value
        default_value = None
        if hasattr(field_info, 'default'):
            default_value = field_info.default
        elif hasattr(field_info, 'default_factory'):
            default_value = field_info.default_factory
        
        # Check if field is required
        is_required = True
        if hasattr(field_info, 'is_required'):
            is_required = field_info.is_required()
        elif default_value is not None:
            is_required = False
        
        param_desc = ParameterDescription(
            name=field_name,
            type=field_type,
            description=description,
            default=default_value,
            required=is_required
        )
        descriptions.append(param_desc)
    
    return descriptions