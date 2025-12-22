class Color:
    """A convenience class to colorize strings in the console.

    Example:
        import
        print("This is {Color.red('important')}.")
    """

    @staticmethod
    def _wrap(code: str, text: str) -> str:
        return f"\033[{code}m{text}\033[0m"

    @staticmethod
    def red(x: str) -> str:
        return Color._wrap("31", x)

    @staticmethod
    def green(x: str) -> str:
        return Color._wrap("32", x)

    @staticmethod
    def cyan(x: str) -> str:
        return Color._wrap("36", x)

    @staticmethod
    def yellow(x: str) -> str:
        return Color._wrap("33", x)