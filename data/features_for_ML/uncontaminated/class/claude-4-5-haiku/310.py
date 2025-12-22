class Config:
    """Pydantic configuration."""
    
    arbitrary_types_allowed = True
    use_enum_values = True
    validate_assignment = True
    allow_population_by_field_name = True
    json_encoders = {}
    case_sensitive = False