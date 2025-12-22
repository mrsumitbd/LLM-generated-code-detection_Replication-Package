def compare(args: argparse.Namespace) -> int:
    if args.file1 == args.file2:
        return 0
    with open(args.file1, 'r') as f1, open(args.file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()
        if content1 == content2:
            return 0
        else:
            return 1