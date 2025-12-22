from typing import Literal

def create_object(
    snowflake_object: SnowflakeObject,
    root: Root,
    mode: Literal["error_if_exists", "replace", "if_not_exists"] = "error_if_exists",
):
    if mode == "error_if_exists":
        # Implement logic for error if object exists
        pass
    elif mode == "replace":
        # Implement logic for replacing object
        pass
    elif mode == "if_not_exists":
        # Implement logic for creating object if it does not exist
        pass