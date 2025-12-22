from argparse import _SubParsersAction

def register_stop_parser(subparsers: _SubParsersAction) -> None:
    """
    Register the 'stop' subcommand parser.

    The parser accepts optional arguments:
        -f, --force   : Force stop the service.
        -t, --timeout : Timeout in seconds (default: 30).

    The parsed arguments are passed to a default handler that currently
    performs no action.  This placeholder can be replaced with the actual
    stop logic elsewhere in the application.
    """
    parser = subparsers.add_parser(
        "stop",
        help="Stop the service",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force stop the service",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds (default: 30)",
    )
    # Default handler placeholder
    parser.set_defaults(func=lambda args: None)