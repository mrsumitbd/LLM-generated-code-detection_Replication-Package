import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class MemrefConstInfo:
    """Holds the parts of a `<var>.<mem at off> op <const number>` expression where op is either `=` or `==`."""
    var: str
    mem: str
    off: str
    op: str
    const: str

    @classmethod
    def from_string(cls, expr: str) -> Optional['MemrefConstInfo']:
        """Parse a memref constant expression and return a MemrefConstInfo object if valid."""
        pattern = r'(\w+)\.(\w+)\s*at\s*(\w+)\s*(==?)\s*(-?\d+)'
        match = re.match(pattern, expr.strip())
        if match:
            var, mem, off, op, const = match.groups()
            return cls(var=var, mem=mem, off=off, op=op, const=const)
        return None

    def __str__(self) -> str:
        """Return the string representation of the memref constant expression."""
        return f"{self.var}.{self.mem} at {self.off} {self.op} {self.const}"

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            'var': self.var,
            'mem': self.mem,
            'off': self.off,
            'op': self.op,
            'const': self.const
        }


if __name__ == "__main__":
    info = MemrefConstInfo(var="x", mem="data", off="0", op="==", const="42")
    print(info)
    print(info.to_dict())

    parsed = MemrefConstInfo.from_string("x.data at 0 == 42")
    if parsed:
        print(parsed)
        print(parsed.to_dict())