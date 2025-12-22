class PatternRule:
    """Represents a composable sequence pattern rule"""

    def __init__(self, operations: list[Operation], parameters: list[int], subrules: list["PatternRule"] = None):
        self.operations = operations
        self.parameters = parameters
        self.subrules = subrules if subrules else []

    def apply(self, sequence: list[int], position: int) -> int:
        for operation, param in zip(self.operations, self.parameters):
            position = operation.apply(sequence, position, param)
        for subrule in self.subrules:
            position = subrule.apply(sequence, position)
        return position

    @classmethod
    def compose(cls, rules: list["PatternRule"]) -> "PatternRule":
        operations = []
        parameters = []
        subrules = []
        for rule in rules:
            operations.extend(rule.operations)
            parameters.extend(rule.parameters)
            subrules.extend(rule.subrules)
        return cls(operations, parameters, subrules)

    def to_string(self) -> str:
        rule_str = ", ".join(f"{op.name}({param})" for op, param in zip(self.operations, self.parameters))
        if self.subrules:
            sub_str = ", ".join(rule.to_string() for rule in self.subrules)
            return f"[{rule_str}, {sub_str}]"
        else:
            return f"[{rule_str}]"