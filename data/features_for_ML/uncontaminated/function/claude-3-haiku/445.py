def create_object(
    snowflake_object: SnowflakeObject,
    root: Root,
    mode: Literal["error_if_exists", "replace", "if_not_exists"] = "error_if_exists",
):
    if mode == "error_if_exists":
        if root.get_object(snowflake_object.name) is not None:
            raise ValueError(f"Object '{snowflake_object.name}' already exists.")
        root.add_object(snowflake_object)
    elif mode == "replace":
        existing_object = root.get_object(snowflake_object.name)
        if existing_object is not None:
            root.remove_object(existing_object)
        root.add_object(snowflake_object)
    elif mode == "if_not_exists":
        if root.get_object(snowflake_object.name) is None:
            root.add_object(snowflake_object)
    else:
        raise ValueError(f"Invalid mode: {mode}")