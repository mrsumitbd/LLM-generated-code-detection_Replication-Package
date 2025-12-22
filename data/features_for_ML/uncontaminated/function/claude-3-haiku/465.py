def extract_required(schema, prefix=""):
    required_fields = []
    for field, field_schema in schema.items():
        if prefix:
            field_name = f"{prefix}.{field}"
        else:
            field_name = field

        if field_schema.get("required", False):
            required_fields.append(field_name)
        elif "properties" in field_schema:
            required_fields.extend(extract_required(field_schema["properties"], field_name))
    return required_fields