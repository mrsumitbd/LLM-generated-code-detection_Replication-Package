class DevopsCopilotCli:
    """
    A simple CLI helper that prints styled text to the terminal.
    Supports basic ANSI styles such as colors, bold, underline, and reset.
    """

    # ANSI escape codes for common styles
    _STYLE_CODES = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        # Bright variants
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",
    }

    def __init__(self) -> None:
        """
        Initialize the CLI helper. No external dependencies are required.
        """
        # No state needed for now; placeholder for future extensions.
        pass

    def print_styled(self, content: str, style: str = ""):
        """
        Print the given content to stdout with the specified ANSI style(s).

        Parameters
        ----------
        content : str
            The text to print.
        style : str, optional
            A space‑separated list of style names (e.g., "red bold").
            If empty or unknown styles are provided, they are ignored.

        Examples
        --------
        >>> cli = DevopsCopilotCli()
        >>> cli.print_styled("Hello, world!", "green bold")
        """
        if not content:
            return

        # Build the ANSI prefix from the requested styles
        codes = []
        for part in style.split():
            code = self._STYLE_CODES.get(part.lower())
            if code:
                codes.append(code)

        # If no valid styles were found, just print the content
        if not codes:
            print(content)
            return

        # Join the codes and reset at the end
        prefix = "".join(codes)
        reset = self._STYLE_CODES["reset"]
        print(f"{prefix}{content}{reset}")