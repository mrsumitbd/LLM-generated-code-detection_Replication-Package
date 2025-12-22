def register_stop_parser(subparsers: _SubParsersAction) -> None:
    """Register the 'stop' subcommand parser."""
    stop_parser = subparsers.add_parser(
        'stop',
        help='Stop the running agent'
    )
    stop_parser.set_defaults(func=stop_agent)