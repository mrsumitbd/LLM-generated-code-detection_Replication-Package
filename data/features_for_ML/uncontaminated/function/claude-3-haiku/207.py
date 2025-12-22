import jsonschema

def load_validator(resource_type_name: str, resource_schema: dict):
    """
    Loads a JSON schema validator for the given resource type.

    Args:
        resource_type_name (str): The name of the resource type.
        resource_schema (dict): The JSON schema for the resource type.

    Returns:
        callable: A function that can validate a given resource against the schema.
    """
    validator = jsonschema.Draft7Validator(resource_schema)

    def validate_resource(resource: dict) -> None:
        """
        Validates a resource against the loaded schema.

        Args:
            resource (dict): The resource to be validated.

        Raises:
            jsonschema.exceptions.ValidationError: If the resource is invalid according to the schema.
        """
        try:
            validator.validate(resource)
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Invalid {resource_type_name} resource: {e}") from e

    return validate_resource