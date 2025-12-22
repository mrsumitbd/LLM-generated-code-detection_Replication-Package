import os
import sys
import time
from colorama import Fore, Style

def display_splash_screen(args: argparse.Namespace) -> None:
    """
    Display a colorful splash screen showing MiniRAG server configuration

    Args:
        args: Parsed command line arguments
    """
    os.system('clear')  # Clear the terminal screen

    print(Fore.CYAN + r"""
    ███████╗██╗   ██╗███╗   ███╗██████╗ ██╗     ███████╗
    ██╔════╝██║   ██║████╗ ████║██╔══██╗██║     ██╔════╝
    █████╗  ██║   ██║██╔████╔██║██████╔╝██║     █████╗
    ██╔══╝  ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝
    ██║     ╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗
    ╚═╝      ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝
    """ + Style.RESET_ALL)

    print(Fore.YELLOW + f"MiniRAG Server Configuration:" + Style.RESET_ALL)
    print(f"  Server Address: {args.server_address}")
    print(f"  Server Port: {args.server_port}")
    print(f"  Database Path: {args.database_path}")
    print(f"  Log Level: {args.log_level}")

    time.sleep(3)  # Wait for 3 seconds before clearing the screen
    os.system('clear')  # Clear the terminal screen again