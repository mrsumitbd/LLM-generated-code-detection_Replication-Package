import argparse

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=str, required=True, help="Input file path")
    parser.add_argument("--output-file", type=str, required=True, help="Output file path")
    parser.add_argument("--max-length", type=int, default=100, help="Maximum length of the output")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    return parser.parse_args(argv)