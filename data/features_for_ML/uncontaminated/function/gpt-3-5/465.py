def extract_required(schema, prefix=""):
    required_fields = []
    
    if isinstance(schema, dict):
        for key, value in schema.items():
            if key == "required" and value:
                required_fields.extend([prefix + "." + field for field in value])
            else:
                required_fields.extend(extract_required(value, prefix + "." + key))
    
    return required_fields