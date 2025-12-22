def function_signature(self) -> str:
        """Returns the function signature as a string.

        Gets the string representation of the function's signature, including name, parameters, and return type.

        Args:
            None

        Returns:
            str: A string containing the complete function signature including the function name,
                parameters (if any), return type annotation (if present), and a colon.
        """
        func_def_src = f"def {self.name}"
        if self.parameters is not None:
            func_def_src += self.parameters.source
        if self.return_type:
            func_def_src += " -> " + self.return_type.source
        func_def_src += ":"
        return func_def_src