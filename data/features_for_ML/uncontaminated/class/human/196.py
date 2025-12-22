import termcolor

class Color:
    """A convenience class to colorize strings in the console.

    Example:
        import
        print("This is {Color.red('important')}.")
    """

    @staticmethod
    def red(x: str) -> str:
        return termcolor.colored(str(x), color="red")

    @staticmethod
    def green(x: str) -> str:
        return termcolor.colored(str(x), color="green")

    @staticmethod
    def cyan(x: str) -> str:
        return termcolor.colored(str(x), color="cyan")

    @staticmethod
    def yellow(x: str) -> str:
        return termcolor.colored(str(x), color="yellow")