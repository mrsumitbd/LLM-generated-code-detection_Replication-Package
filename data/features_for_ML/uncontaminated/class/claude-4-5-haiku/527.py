class PatternRule:
    """Represents a composable sequence pattern rule"""

    def __init__(self, operations: list[Operation], parameters: list[int], subrules: list["PatternRule"] = None):
        self.operations = operations
        self.parameters = parameters
        self.subrules = subrules if subrules is not None else []

    def apply(self, sequence: list[int], position: int) -> int:
        result = sequence[position] if position < len(sequence) else 0
        
        for i, operation in enumerate(self.operations):
            param = self.parameters[i] if i < len(self.parameters) else 0
            
            if self.subrules and i < len(self.subrules):
                subrule_result = self.subrules[i].apply(sequence, position)
                result = operation.execute(result, subrule_result)
            else:
                result = operation.execute(result, param)
        
        return result

    @classmethod
    def compose(cls, rules: list["PatternRule"]) -> "PatternRule":
        if not rules:
            return cls([], [])
        
        if len(rules) == 1:
            return rules[0]
        
        all_operations = []
        all_parameters = []
        all_subrules = []
        
        for rule in rules:
            all_operations.extend(rule.operations)
            all_parameters.extend(rule.parameters)
            all_subrules.extend(rule.subrules)
        
        return cls(all_operations, all_parameters, all_subrules)

    def to_string(self) -> str:
        parts = []
        
        for i, operation in enumerate(self.operations):
            param = self.parameters[i] if i < len(self.parameters) else 0
            
            if self.subrules and i < len(self.subrules):
                subrule_str = self.subrules[i].to_string()
                parts.append(f"{operation.__class__.__name__}({subrule_str})")
            else:
                parts.append(f"{operation.__class__.__name__}({param})")
        
        return " -> ".join(parts) if parts else "empty"