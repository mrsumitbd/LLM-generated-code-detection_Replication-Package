def function_signature(self) -> str:
    """Returns the function signature as a string.

    Gets the string representation of the function's signature, including name, parameters, and return type.

    Args:
        None

    Returns:
        str: A string containing the complete function signature including the function name,
            parameters (if any), return type annotation (if present), and a colon.
    """
    signature = f"{self.__class__.__name__}.{self.__name__}("
    parameters = []
    for param in inspect.signature(self).parameters.values():
        param_str = param.name
        if param.annotation != inspect.Parameter.empty:
            param_str += f": {param.annotation.__name__}"
        parameters.append(param_str)
    signature += ", ".join(parameters) + ") -> " + (self.__annotations__["return"].__name__ if "return" in self.__annotations__ else "None")
    return signature + ":"