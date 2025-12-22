def to_dict(self) -> Dict[str, Any]:
    """Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    * Fields in `self.additional_properties` are added to the output dict.
    """
    output_dict = {}
    
    # Get the model dump with aliases
    model_dict = self.model_dump(by_alias=True)
    
    # Get fields that were explicitly set
    fields_set = self.model_fields_set if hasattr(self, 'model_fields_set') else set()
    
    # Process each field from the model
    for field_name, field_value in model_dict.items():
        # Find the original field name to check if it was set
        original_field_name = field_name
        for field_key, field_info in self.model_fields.items():
            if field_info.alias == field_name or field_key == field_name:
                original_field_name = field_key
                break
        
        # Include the field if:
        # 1. The value is not None, OR
        # 2. The value is None but the field was explicitly set
        if field_value is not None or original_field_name in fields_set:
            output_dict[field_name] = field_value
    
    # Add additional properties if they exist
    if hasattr(self, 'additional_properties') and self.additional_properties:
        output_dict.update(self.additional_properties)
    
    return output_dict