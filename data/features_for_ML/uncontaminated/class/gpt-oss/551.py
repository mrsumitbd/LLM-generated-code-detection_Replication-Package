import sys
import os

class Colors:
    """Terminal colors for output."""

    # Detect if we should output ANSI codes
    ENABLED = sys.stdout.isatty()

    # On Windows, try to enable ANSI support via colorama
    if os.name == "nt":
        try:
            import colorama

            colorama.init()
        except Exception:
            # If colorama is not available or fails, we simply ignore it
            pass

    # ANSI escape codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    @classmethod
    def enable(cls, enabled: bool = True) -> None:
        """Enable or disable color output."""
        cls.ENABLED = enabled

    @classmethod
    def color(cls, text: str, *codes: str) -> str:
        """Wrap text with the given ANSI codes."""
        if not cls.ENABLED:
            return text
        return "".join(codes) + text + cls.RESET

    # Convenience wrappers for common colors
    @classmethod
    def black(cls, text: str) -> str:
        return cls.color(text, cls.BLACK)

    @classmethod
    def red(cls, text: str) -> str:
        return cls.color(text, cls.RED)

    @classmethod
    def green(cls, text: str) -> str:
        return cls.color(text, cls.GREEN)

    @classmethod
    def yellow(cls, text: str) -> str:
        return cls.color(text, cls.YELLOW)

    @classmethod
    def blue(cls, text: str) -> str:
        return cls.color(text, cls.BLUE)

    @classmethod
    def magenta(cls, text: str) -> str:
        return cls.color(text, cls.MAGENTA)

    @classmethod
    def cyan(cls, text: str) -> str:
        return cls.color(text, cls.CYAN)

    @classmethod
    def white(cls, text: str) -> str:
        return cls.color(text, cls.WHITE)

    # Background color wrappers
    @classmethod
    def bg_black(cls, text: str) -> str:
        return cls.color(text, cls.BG_BLACK)

    @classmethod
    def bg_red(cls, text: str) -> str:
        return cls.color(text, cls.BG_RED)

    @classmethod
    def bg_green(cls, text: str) -> str:
        return cls.color(text, cls.BG_GREEN)

    @classmethod
    def bg_yellow(cls, text: str) -> str:
        return cls.color(text, cls.BG_YELLOW)

    @classmethod
    def bg_blue(cls, text: str) -> str:
        return cls.color(text, cls.BG_BLUE)

    @classmethod
    def bg_magenta(cls, text: str) -> str:
        return cls.color(text, cls.BG_MAGENTA)

    @classmethod
    def bg_cyan(cls, text: str) -> str:
        return cls.color(text, cls.BG_CYAN)

    @classmethod
    def bg_white(cls, text: str) -> str:
        return cls.color(text, cls.BG_WHITE)

    # Style wrappers
    @classmethod
    def bold(cls, text: str) -> str:
        return cls.color(text, cls.BOLD)

    @classmethod
    def underline(cls, text: str) -> str:
        return cls.color(text, cls.UNDERLINE)