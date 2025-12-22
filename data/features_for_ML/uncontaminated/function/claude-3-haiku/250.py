def register_stop_parser(subparsers: _SubParsersAction) -> None:
    stop_parser = subparsers.add_parser("stop", help="Stop the application")
    stop_parser.add_argument("-f", "--force", action="store_true", help="Force stop the application")
    stop_parser.set_defaults(func=stop_application)

def stop_application(args):
    if args.force:
        # Forcefully stop the application
        print("Forcefully stopping the application...")
    else:
        # Gracefully stop the application
        print("Gracefully stopping the application...")