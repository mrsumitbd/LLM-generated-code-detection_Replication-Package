import jsonschema
from jsonschema import Draft7Validator, ValidationError


def load_validator(resource_type_name: str, resource_schema: dict):
    """
    Compile a JSON schema into a validator object.

    Parameters
    ----------
    resource_type_name : str
        Human‑readable name of the resource type (used only for error messages).
    resource_schema : dict
        The JSON schema definition for the resource.

    Returns
    -------
    jsonschema.validators.Validator
        A validator instance that can be used to validate data against the schema.

    Raises
    ------
    ValueError
        If the provided schema is not a valid JSON schema.
    """
    try:
        validator = Draft7Validator(resource_schema)
    except Exception as exc:
        raise ValueError(
            f"Failed to compile JSON schema for resource type '{resource_type_name}': {exc}"
        ) from exc

    # Attach a helper method to the validator for convenience
    def validate(data):
        """
        Validate the given data against the compiled schema.

        Raises
        ------
        jsonschema.exceptions.ValidationError
            If the data does not conform to the schema.
        """
        validator.validate(data)

    validator.validate_data = validate
    return validator