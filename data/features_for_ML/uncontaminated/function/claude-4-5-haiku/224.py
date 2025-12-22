def register_exists_parser(subparsers: _SubParsersAction) -> None:
    """Register the 'exists' subcommand parser."""
    parser = subparsers.add_parser(
        "exists",
        help="Check if a key exists in the database"
    )
    parser.add_argument(
        "key",
        help="The key to check"
    )
    parser.set_defaults(func=exists_command)