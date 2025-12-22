def list_objects_tool(
        object_type: object_type_annotation,
        database_name: str | None = None,
        schema_name: str | None = None,
        like: Annotated[
            str | None,
            Field(
                description="Filter objects by keyword in name. Uses case-insensitive pattern matching, with support for SQL wildcard characters (% and _).",
                default=None,
            ),
        ] = None,
        starts_with: Annotated[
            str | None,
            Field(
                description="Filter objects by start of name. Case sensitive. Ignored for warehouses.",
                default=None,
            ),
        ] = None,
    ):
    """List objects of a given type from Snowflake."""
    
    # Build the SHOW command based on object type
    show_command = f"SHOW {object_type.upper()}"
    
    # Add database and schema context if provided
    if database_name and schema_name:
        show_command += f" IN SCHEMA {database_name}.{schema_name}"
    elif database_name:
        show_command += f" IN DATABASE {database_name}"
    elif schema_name:
        show_command += f" IN SCHEMA {schema_name}"
    
    # Add LIKE filter if provided
    if like:
        show_command += f" LIKE '{like}'"
    
    # Add STARTS_WITH filter if provided (not for warehouses)
    if starts_with and object_type.upper() != "WAREHOUSE":
        show_command += f" STARTS_WITH '{starts_with}'"
    
    # Execute the command and return results
    try:
        results = session.sql(show_command).collect()
        return [row.asDict() for row in results]
    except Exception as e:
        return {"error": str(e)}