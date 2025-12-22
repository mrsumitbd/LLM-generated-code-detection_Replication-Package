def register_exists_parser(subparsers: _SubParsersAction) -> None:
    exists_parser = subparsers.add_parser('exists', help='Check if a file or directory exists')
    exists_parser.add_argument('path', help='Path to the file or directory to check for existence')
    exists_parser.set_defaults(func=exists_command)