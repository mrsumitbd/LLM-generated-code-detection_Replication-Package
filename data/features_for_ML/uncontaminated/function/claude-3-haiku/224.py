def register_exists_parser(subparsers: _SubParsersAction) -> None:
    exists_parser = subparsers.add_parser(
        "exists",
        help="Check if a file or directory exists",
    )
    exists_parser.add_argument(
        "path",
        type=str,
        help="The path to check",
    )
    exists_parser.set_defaults(func=handle_exists)


def handle_exists(args: argparse.Namespace) -> None:
    path = args.path
    if os.path.exists(path):
        print(f"{path} exists")
    else:
        print(f"{path} does not exist")