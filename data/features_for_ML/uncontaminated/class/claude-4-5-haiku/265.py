class Config:
    """SQLModel configuration."""
    
    def __init__(self):
        self.arbitrary_types_allowed = True
        self.json_encoders = {}
        self.validate_assignment = False
        self.use_enum_values = False
        self.allow_population_by_field_name = True
        self.orm_mode = True