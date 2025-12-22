def compare(args: argparse.Namespace) -> int:
    if args.a > args.b:
        return 1
    elif args.a < args.b:
        return -1
    else:
        return 0