def create_object(
    snowflake_object: SnowflakeObject,
    root: Root,
    mode: Literal["error_if_exists", "replace", "if_not_exists"] = "error_if_exists",
):
    """
    Create a Snowflake object with the specified mode.
    
    Args:
        snowflake_object: The Snowflake object to create
        root: The root configuration object
        mode: How to handle existing objects
            - "error_if_exists": Raise an error if object exists
            - "replace": Replace existing object
            - "if_not_exists": Skip if object exists
    """
    object_type = snowflake_object.get_type()
    object_name = snowflake_object.get_name()
    
    # Check if object exists
    object_exists = snowflake_object.exists(root)
    
    if object_exists:
        if mode == "error_if_exists":
            raise ValueError(f"{object_type} '{object_name}' already exists")
        elif mode == "replace":
            snowflake_object.drop(root)
        elif mode == "if_not_exists":
            return
    
    # Create the object
    snowflake_object.create(root)