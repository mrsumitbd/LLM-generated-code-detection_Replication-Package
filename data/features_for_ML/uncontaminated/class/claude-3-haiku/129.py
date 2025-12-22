class LibraryFunctionCompiler:
    def __init__(self, name, type, parameters, code):
        self.name = name
        self.type = type
        self.parameters = parameters
        self.code = code

    def get_code(self, current_stack_pointer):
        code = []
        for param in self.parameters:
            code.append(f"LOAD {current_stack_pointer} {param}")
            current_stack_pointer += 1
        code.extend(self.code)
        return code, current_stack_pointer