class ColorCodes:
    """
    Color codes for rich text output
    """

    # Reset and style codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"

    @staticmethod
    def wrap(text: str, *codes: str) -> str:
        """
        Wrap the given text with the provided ANSI codes and reset at the end.
        """
        return "".join(codes) + text + ColorCodes.RESET

    @staticmethod
    def color(text: str, fg: str | None = None, bg: str | None = None, style: str | None = None) -> str:
        """
        Apply foreground, background, and style codes to the text.
        """
        parts = []
        if style:
            parts.append(getattr(ColorCodes, style.upper(), ""))
        if fg:
            parts.append(getattr(ColorCodes, fg.upper(), ""))
        if bg:
            parts.append(getattr(ColorCodes, f"BG_{bg.upper()}", ""))
        return ColorCodes.wrap(text, *parts)

    @staticmethod
    def bold(text: str) -> str:
        return ColorCodes.wrap(text, ColorCodes.BOLD)

    @staticmethod
    def underline(text: str) -> str:
        return ColorCodes.wrap(text, ColorCodes.UNDERLINE)

    @staticmethod
    def bright(text: str) -> str:
        return ColorCodes.wrap(text, ColorCodes.BRIGHT_WHITE)

    @staticmethod
    def reset() -> str:
        return ColorCodes.RESET