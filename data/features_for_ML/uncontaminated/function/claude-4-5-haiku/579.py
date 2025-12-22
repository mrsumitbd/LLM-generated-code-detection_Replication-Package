import argparse

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Parse command line arguments')
    parser.add_argument('--help', '-h', action='help', help='show this help message and exit')
    return parser.parse_args(argv)