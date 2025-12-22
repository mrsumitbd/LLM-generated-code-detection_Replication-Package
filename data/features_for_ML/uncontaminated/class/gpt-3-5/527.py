from typing import List

class PatternRule:
    """Represents a composable sequence pattern rule"""

    def __init__(self, operations: List[Operation], parameters: List[int], subrules: List["PatternRule"] = None):
        self.operations = operations
        self.parameters = parameters
        self.subrules = subrules if subrules is not None else []

    def apply(self, sequence: List[int], position: int) -> int:
        result = position
        for operation, parameter in zip(self.operations, self.parameters):
            if operation == Operation.ADD:
                result += parameter
            elif operation == Operation.SUBTRACT:
                result -= parameter
            elif operation == Operation.MULTIPLY:
                result *= parameter
            elif operation == Operation.DIVIDE:
                result //= parameter
        for subrule in self.subrules:
            result = subrule.apply(sequence, result)
        return result

    @classmethod
    def compose(cls, rules: List["PatternRule"]) -> "PatternRule":
        operations = []
        parameters = []
        subrules = []
        for rule in rules:
            operations.extend(rule.operations)
            parameters.extend(rule.parameters)
            subrules.extend(rule.subrules)
        return PatternRule(operations, parameters, subrules)

    def to_string(self) -> str:
        return f"Operations: {self.operations}, Parameters: {self.parameters}, Subrules: {self.subrules}"

class Operation:
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"