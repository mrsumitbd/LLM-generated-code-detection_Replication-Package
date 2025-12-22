class MemrefConstInfo:
    """Holds the parts of a `<var>.<mem at off> op <const number>` expression where op is either `=` or `==`."""

    def __init__(self, var, mem_offset, op, const_value):
        self.var = var
        self.mem_offset = mem_offset
        self.op = op
        self.const_value = const_value

    def __str__(self):
        return f"{self.var}.{self.mem_offset} {self.op} {self.const_value}"

    def __eq__(self, other):
        return (
            self.var == other.var
            and self.mem_offset == other.mem_offset
            and self.op == other.op
            and self.const_value == other.const_value
        )

    def __hash__(self):
        return hash((self.var, self.mem_offset, self.op, self.const_value))