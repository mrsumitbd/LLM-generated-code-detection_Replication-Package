import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MemrefConstInfo:
    """
    Holds the parts of a `<var>.<mem at off> op <const number>` expression where
    op is either `=` or `==`.

    Examples of supported syntax:

        x.mem[10] = 5
        y.mem at 20 == -3
        z.foo[0] == 42
    """

    var: str
    mem: str
    offset: int
    op: str
    const: int

    _PATTERN = re.compile(
        r"""
        ^\s*
        (?P<var>\w+)\.                # variable name
        (?P<mem>\w+)                  # memory field name
        \s*
        (?:\[\s*(?P<offset>\d+)\s*\]   # [offset]
        |at\s+(?P<offset2>\d+))       # or at offset
        \s*
        (?P<op>=|==)                  # operator
        \s*
        (?P<const>-?\d+)              # constant (int, optional sign)
        \s*$
        """,
        re.VERBOSE,
    )

    @classmethod
    def parse(cls, expr: str) -> "MemrefConstInfo":
        """
        Parse an expression string and return a MemrefConstInfo instance.

        Raises ValueError if the expression does not match the expected pattern.
        """
        m = cls._PATTERN.match(expr)
        if not m:
            raise ValueError(f"Invalid memref‑const expression: {expr!r}")

        var = m.group("var")
        mem = m.group("mem")
        offset = m.group("offset") or m.group("offset2")
        op = m.group("op")
        const = m.group("const")

        return cls(
            var=var,
            mem=mem,
            offset=int(offset),
            op=op,
            const=int(const),
        )

    def __str__(self) -> str:
        """Return a canonical string representation."""
        return f"{self.var}.{self.mem}[{self.offset}] {self.op} {self.const}"

    def __repr__(self) -> str:
        return (
            f"MemrefConstInfo(var={self.var!r}, mem={self.mem!r}, "
            f"offset={self.offset!r}, op={self.op!r}, const={self.const!r})"
        )

    def to_dict(self) -> dict:
        """Return a dictionary representation of the instance."""
        return {
            "var": self.var,
            "mem": self.mem,
            "offset": self.offset,
            "op": self.op,
            "const": self.const,
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MemrefConstInfo):
            return NotImplemented
        return (
            self.var == other.var
            and self.mem == other.mem
            and self.offset == other.offset
            and self.op == other.op
            and self.const == other.const
        )