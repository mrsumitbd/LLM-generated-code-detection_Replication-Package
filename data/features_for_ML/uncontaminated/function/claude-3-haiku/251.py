from typing import NamedTuple

class Arg(NamedTuple):
    name: str
    value: str

def parse_as_attr(arg: str) -> Arg:
    name, value = arg.split('=', 1)
    return Arg(name.strip(), value.strip())