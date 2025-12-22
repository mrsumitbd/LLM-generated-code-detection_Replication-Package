class PatternRule:
    """Represents a composable sequence pattern rule"""

    def __init__(self, operations: list, parameters: list[int], subrules: list["PatternRule"] = None):
        """
        :param operations: list of operation objects or callables
        :param parameters: list of integer parameters for the operations
        :param subrules: optional list of nested PatternRule objects
        """
        self.operations = operations or []
        self.parameters = parameters or []
        self.subrules = subrules or []

    def _apply_operation(self, op, seq, pos, param):
        """
        Helper to apply a single operation. Supports objects with an `apply`
        method or plain callables.
        """
        if hasattr(op, "apply") and callable(op.apply):
            return op.apply(seq, pos, param)
        if callable(op):
            return op(seq, pos, param)
        raise TypeError(f"Unsupported operation type: {type(op)}")

    def apply(self, sequence: list[int], position: int) -> int:
        """
        Apply the rule to the given sequence starting at `position`.
        Returns the new position after all operations and subrules have been applied.
        """
        pos = position
        # Apply each operation with its corresponding parameter
        for op, param in zip(self.operations, self.parameters):
            pos = self._apply_operation(op, sequence, pos, param)
        # Apply each subrule sequentially
        for sub in self.subrules:
            pos = sub.apply(sequence, pos)
        return pos

    @classmethod
    def compose(cls, rules: list["PatternRule"]) -> "PatternRule":
        """
        Compose multiple PatternRule objects into a single rule that applies
        them in sequence. The composed rule has no direct operations; it
        delegates to the subrules.
        """
        return cls([], [], rules)

    def to_string(self) -> str:
        """
        Return a human‑readable representation of the rule.
        """
        parts = []

        if self.operations:
            ops_repr = ", ".join(
                f"{op.__class__.__name__}({p})" if hasattr(op, "__class__") else f"{op}({p})"
                for op, p in zip(self.operations, self.parameters)
            )
            parts.append(f"Ops[{ops_repr}]")

        if self.subrules:
            subs_repr = ", ".join(sub.to_string() for sub in self.subrules)
            parts.append(f"Subs[{subs_repr}]")

        return " | ".join(parts) if parts else "EmptyRule"