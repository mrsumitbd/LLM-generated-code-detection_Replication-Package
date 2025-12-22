def register_stop_parser(subparsers: _SubParsersAction) -> None:
    stop_parser = subparsers.add_parser('stop', help='Stop the process')
    stop_parser.set_defaults(func=stop_process)