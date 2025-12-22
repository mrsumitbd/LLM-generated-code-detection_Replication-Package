class Color:
    """A convenience class to colorize strings in the console.

    Example:
        import
        print("This is {Color.red('important')}.")
    """

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"

    @staticmethod
    def red(x: str) -> str:
        return f"{Color.RED}{x}{Color.RESET}"

    @staticmethod
    def green(x: str) -> str:
        return f"{Color.GREEN}{x}{Color.RESET}"

    @staticmethod
    def cyan(x: str) -> str:
        return f"{Color.CYAN}{x}{Color.RESET}"

    @staticmethod
    def yellow(x: str) -> str:
        return f"{Color.YELLOW}{x}{Color.RESET}"