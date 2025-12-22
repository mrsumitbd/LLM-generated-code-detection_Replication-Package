def to_dict(self) -> Dict[str, Any]:
    """Return the dictionary representation of the model using alias.

    This has the following differences from calling pydantic's
    `self.model_dump(by_alias=True)`:

    * `None` is only added to the output dict for nullable fields that
      were set at model initialization. Other fields with value `None`
      are ignored.
    """
    output = {}
    
    for field_name, field_info in self.model_fields.items():
        value = getattr(self, field_name)
        
        # Get the alias for the field, or use the field name if no alias
        key = field_info.alias if field_info.alias else field_name
        
        # Skip None values unless the field was explicitly set and is nullable
        if value is None:
            # Check if field was set in the model's fields_set
            if field_name in self.model_fields_set:
                # Include None only if the field is nullable
                if field_info.is_required() is False or field_info.default is None:
                    output[key] = value
        else:
            output[key] = value
    
    return output