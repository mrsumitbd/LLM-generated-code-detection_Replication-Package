class LibraryFunctionCompiler:
    """
    A simple compiler helper for library functions.

    Parameters
    ----------
    name : str
        The name of the library function.
    type : str
        The return type of the library function.
    parameters : list[str]
        A list of parameter names (or types) for the function.
    code : str
        The body of the function as a string. It may contain
        placeholders that will be replaced when `get_code` is called.
    """

    def __init__(self, name, type, parameters, code):
        self.name = name
        self.type = type
        self.parameters = parameters
        self.code = code

    def get_code(self, current_stack_pointer):
        """
        Return the compiled code for the library function.

        The `current_stack_pointer` is inserted into the code template
        if the placeholder `{current_stack_pointer}` is present.

        Returns
        -------
        str
            The formatted code string.
        """
        # Prepare a dictionary of values that can be used in the format string.
        format_dict = {
            "name": self.name,
            "type": self.type,
            "parameters": ", ".join(self.parameters),
            "current_stack_pointer": current_stack_pointer,
        }
        # Use str.format_map to avoid KeyError if a placeholder is missing.
        return self.code.format_map(format_dict)