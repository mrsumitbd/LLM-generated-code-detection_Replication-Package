class Color:
    """A convenience class to colorize strings in the console.

    Example:
        import
        print("This is {Color.red('important')}.")
    """

    @staticmethod
    def red(x: str) -> str:
        return f"\033[91m{x}\033[0m"

    @staticmethod
    def green(x: str) -> str:
        return f"\033[92m{x}\033[0m"

    @staticmethod
    def cyan(x: str) -> str:
        return f"\033[96m{x}\033[0m"

    @staticmethod
    def yellow(x: str) -> str:
        return f"\033[93m{x}\033[0m"