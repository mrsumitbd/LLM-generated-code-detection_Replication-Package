def parse_as_attr(arg: str) -> Arg:
    class Arg:
        def __init__(self, value):
            self.value = value

    return Arg(arg)