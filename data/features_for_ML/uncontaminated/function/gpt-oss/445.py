from typing import Literal

def create_object(
    snowflake_object: "SnowflakeObject",
    root: "Root",
    mode: Literal["error_if_exists", "replace", "if_not_exists"] = "error_if_exists",
):
    """
    Create a Snowflake object (table, view, schema, etc.) using the provided
    SnowflakeObject definition and the Root session.

    Parameters
    ----------
    snowflake_object : SnowflakeObject
        Object containing the definition and metadata for the Snowflake object.
    root : Root
        Root instance that provides a Snowflake session via `root.session`.
    mode : Literal["error_if_exists", "replace", "if_not_exists"]
        Creation mode:
            * "error_if_exists"  – raise an error if the object already exists.
            * "replace"          – drop the object if it exists, then create it.
            * "if_not_exists"    – create the object only if it does not already exist.

    Returns
    -------
    None
    """
    # Helper to quote identifiers
    def quote(id_: str) -> str:
        return f'"{id_}"'

    # Resolve schema and name
    schema = getattr(snowflake_object, "schema", None)
    name = getattr(snowflake_object, "name")
    obj_type = getattr(snowflake_object, "type", None)

    if not obj_type or not name:
        raise ValueError("SnowflakeObject must have 'type' and 'name' attributes")

    # Build fully qualified name
    if schema:
        full_name = f"{quote(schema)}.{quote(name)}"
    else:
        # If no schema provided, use the current session schema
        try:
            current_schema = root.session.get_current_schema()
        except Exception:
            current_schema = None
        if current_schema:
            full_name = f"{quote(current_schema)}.{quote(name)}"
        else:
            full_name = quote(name)

    # Determine existence
    exists = False
    try:
        # Use SHOW <type>s LIKE '<name>' IN SCHEMA <schema>
        show_sql = f"SHOW {obj_type}s LIKE '{name}'"
        if schema:
            show_sql += f" IN SCHEMA {quote(schema)}"
        cursor = root.session.execute(show_sql)
        # SHOW returns a result set; if any rows, the object exists
        exists = cursor.rowcount > 0
    except Exception:
        # If SHOW fails (e.g., unsupported type), fall back to INFORMATION_SCHEMA
        try:
            if obj_type.upper() == "TABLE":
                info_sql = (
                    f"SELECT 1 FROM information_schema.tables "
                    f"WHERE table_name = '{name}'"
                )
            elif obj_type.upper() == "VIEW":
                info_sql = (
                    f"SELECT 1 FROM information_schema.views "
                    f"WHERE table_name = '{name}'"
                )
            else:
                # Generic fallback: try tables
                info_sql = (
                    f"SELECT 1 FROM information_schema.tables "
                    f"WHERE table_name = '{name}'"
                )
            if schema:
                info_sql += f" AND table_schema = '{schema}'"
            cursor = root.session.execute(info_sql)
            exists = cursor.rowcount > 0
        except Exception:
            # If all checks fail, assume it does not exist
            exists = False

    # Build the CREATE statement
    try:
        create_sql = snowflake_object.get_create_sql()
    except Exception:
        # Fallback: construct a simple CREATE if possible
        create_sql = f"CREATE {obj_type} {full_name}"

    # Execute based on mode
    if mode == "error_if_exists":
        if exists:
            raise ValueError(f"{obj_type} {full_name} already exists")
        root.session.execute(create_sql)

    elif mode == "replace":
        if exists:
            drop_sql = f"DROP {obj_type} IF EXISTS {full_name}"
            root.session.execute(drop_sql)
        root.session.execute(create_sql)

    elif mode == "if_not_exists":
        if exists:
            # Nothing to do
            return
        root.session.execute(create_sql)

    else:
        raise ValueError(f"Unsupported mode: {mode}")