class LibraryFunctionCompiler:

    def __init__(self, name, type, parameters, code):
        self.name = name
        self.type = type
        self.parameters = parameters
        self.code = code

    def get_code(self, current_stack_pointer):
        compiled_code = []
        
        # Function prologue
        compiled_code.append(f"# Function: {self.name}")
        compiled_code.append(f"{self.name}:")
        compiled_code.append("push rbp")
        compiled_code.append("mov rbp, rsp")
        
        # Calculate local variable space needed
        local_space = current_stack_pointer
        if local_space > 0:
            compiled_code.append(f"sub rsp, {local_space}")
        
        # Function body
        if isinstance(self.code, list):
            compiled_code.extend(self.code)
        else:
            compiled_code.append(self.code)
        
        # Function epilogue
        compiled_code.append("mov rsp, rbp")
        compiled_code.append("pop rbp")
        compiled_code.append("ret")
        
        return "\n".join(compiled_code)