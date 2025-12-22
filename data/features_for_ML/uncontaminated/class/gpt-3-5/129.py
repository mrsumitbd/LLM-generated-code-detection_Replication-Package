class LibraryFunctionCompiler:

    def __init__(self, name, type, parameters, code):
        self.name = name
        self.type = type
        self.parameters = parameters
        self.code = code

    def get_code(self, current_stack_pointer):
        return f"{self.type} {self.name}({', '.join(self.parameters)}) {{\n{self.code}\n}}"