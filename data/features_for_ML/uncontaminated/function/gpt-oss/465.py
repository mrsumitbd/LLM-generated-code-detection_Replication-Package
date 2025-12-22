def extract_required(schema, prefix=""):
    """
    Recursively extract all required field names from a JSON schema.
    The returned names are prefixed with the provided `prefix` and
    separated by dots for nested objects.

    Parameters
    ----------
    schema : dict
        A JSON schema dictionary.
    prefix : str, optional
        A string to prepend to each field name (used for recursion).

    Returns
    -------
    list[str]
        A list of required field names with prefixes.
    """
    required_fields = []

    if not isinstance(schema, dict):
        return required_fields

    # Handle required fields at the current level
    req = schema.get("required")
    if isinstance(req, list):
        for field in req:
            # Build the full field name
            full_name = f"{prefix}{field}" if prefix else field
            required_fields.append(full_name)

            # Recurse into the field's subschema if it exists
            subschema = schema.get("properties", {}).get(field)
            if subschema:
                sub_prefix = f"{full_name}."
                required_fields.extend(extract_required(subschema, sub_prefix))

    # Handle array items (if the schema is an array)
    if schema.get("type") == "array":
        items = schema.get("items")
        if items:
            required_fields.extend(extract_required(items, prefix))

    # Handle composed schemas (allOf, anyOf, oneOf)
    for key in ("allOf", "anyOf", "oneOf"):
        if key in schema and isinstance(schema[key], list):
            for subschema in schema[key]:
                required_fields.extend(extract_required(subschema, prefix))

    return required_fields