import argparse
import sys

def parse_args():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generic command-line argument parser."
    )

    # Positional arguments (optional)
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Input file path (optional)."
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Output file path (optional)."
    )

    # Optional flags
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output."
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="Path to configuration file."
    )

    # Optional version flag
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0",
        help="Show program's version number and exit."
    )

    # Parse arguments from sys.argv
    return parser.parse_args()