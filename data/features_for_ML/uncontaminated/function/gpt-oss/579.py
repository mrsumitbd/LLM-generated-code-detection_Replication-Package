import argparse

def parse_args(argv: list[str]) -> argparse.Namespace:
    """
    Parse command‑line arguments.

    The parser accepts the following options:

    * ``-c`` / ``--config`` – Path to a configuration file.
    * ``-v`` / ``--verbose`` – Enable verbose output.
    * Positional ``files`` – Zero or more input file names.

    Parameters
    ----------
    argv : list[str]
        The list of command‑line arguments (excluding the program name).

    Returns
    -------
    argparse.Namespace
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process input files with optional configuration."
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Path to a configuration file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Input file names",
    )
    return parser.parse_args(argv)