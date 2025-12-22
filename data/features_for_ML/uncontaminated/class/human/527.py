
class PatternRule:
    """Represents a composable sequence pattern rule"""

    def __init__(self, operations: list[Operation], parameters: list[int], subrules: list["PatternRule"] = None):
        self.operations = operations
        self.parameters = parameters
        self.subrules = subrules or []

    def apply(self, sequence: list[int], position: int) -> int:
        """Apply the rule to generate the next number"""
        result = sequence[position]  # Start with current number

        for op, param in zip(self.operations, self.parameters):
            if op == Operation.ADD:
                result += param
            elif op == Operation.MULTIPLY:
                result *= param
            elif op == Operation.SQUARE:
                result = result * result
            elif op == Operation.DOUBLE:
                result *= 2
            elif op == Operation.HALF:
                result //= 2  # Integer division
            elif op == Operation.PREV_PLUS:
                if position > 0:
                    result += sequence[position - 1]
            elif op == Operation.COMPOSE:
                # Apply each subrule in sequence, passing the result through
                for subrule in self.subrules:
                    temp_sequence = sequence[: position + 1]
                    temp_sequence[-1] = result  # Use current result as input
                    result = subrule.apply(temp_sequence, position)

        return result

    @classmethod
    def compose(cls, rules: list["PatternRule"]) -> "PatternRule":
        """Create a new rule that composes multiple rules together"""
        return cls([Operation.COMPOSE], [0], subrules=rules)

    def to_string(self) -> str:
        """Convert rule to human-readable string"""
        parts = []
        for op, param in zip(self.operations, self.parameters):
            if op == Operation.ADD:
                parts.append(f"add {param}")
            elif op == Operation.MULTIPLY:
                parts.append(f"multiply by {param}")
            elif op == Operation.SQUARE:
                parts.append("square")
            elif op == Operation.DOUBLE:
                parts.append("double")
            elif op == Operation.HALF:
                parts.append("halve")
            elif op == Operation.PREV_PLUS:
                parts.append("add previous")
        return " then ".join(parts)