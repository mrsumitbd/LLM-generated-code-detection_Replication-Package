import fastjsonschema

def load_validator(resource_type_name: str, resource_schema: dict):
    spec = resource_schema.get("spec")
    if not spec:
        return None

    spec_names = spec.get("names")
    if spec_names:
        spec_kind = spec_names.get("kind", "<missing kind>")
    else:
        spec_kind = "<missing kind>"

    schema_specs = spec.get("versions")
    if not schema_specs:
        return None

    for schema_spec in schema_specs:
        version = schema_spec.get("name")
        if not version:
            continue

        schema_block = schema_spec.get("schema")
        if not schema_block:
            continue

        openapi_schema = schema_block.get("openAPIV3Schema")
        if not openapi_schema:
            continue

        openapi_properties = openapi_schema.get("properties")
        if not openapi_properties:
            continue

        openapi_spec = openapi_properties.get("spec")

        try:
            version_validator = fastjsonschema.compile(openapi_spec)
        except fastjsonschema.JsonSchemaDefinitionException:
            logger.exception(f"Failed to process {spec_kind} {version}")
            continue
        except AttributeError as err:
            logger.error(
                f"Probably encountered an empty `properties` block for {spec_kind} {version} (err: {err})"
            )
            raise

        resource_version_key = f"{resource_type_name}:{version}"
        _SCHEMA_VALIDATORS[resource_version_key] = version_validator