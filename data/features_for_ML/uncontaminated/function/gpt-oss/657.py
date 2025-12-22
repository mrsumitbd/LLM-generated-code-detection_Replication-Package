import argparse
from typing import Any

try:
    from colorama import init, Fore, Style
except ImportError:
    # Fallback if colorama is not available
    class _Dummy:
        def __getattr__(self, name):
            return ""

    init = lambda *_, **__: None
    Fore = Style = _Dummy()

def display_splash_screen(args: argparse.Namespace) -> None:
    """
    Display a colorful splash screen showing MiniRAG server configuration

    Args:
        args: Parsed command line arguments
    """
    init(autoreset=True)

    # Basic banner
    banner = f"{Fore.CYAN}{Style.BRIGHT}=== MiniRAG Server ==={Style.RESET_ALL}"
    print("\n" + banner)

    # Separator
    print(f"{Fore.YELLOW}{'-' * 30}{Style.RESET_ALL}")

    # Display each argument in a key: value format
    for key in sorted(vars(args)):
        value: Any = getattr(args, key)
        # Convert complex objects to string
        if isinstance(value, (list, tuple)):
            value_str = ", ".join(map(str, value))
        else:
            value_str = str(value)
        print(f"{Fore.CYAN}{key:<15}{Style.RESET_ALL}{Fore.GREEN}{value_str}{Style.RESET_ALL}")

    # Final separator
    print(f"{Fore.YELLOW}{'-' * 30}{Style.RESET_ALL}\n")