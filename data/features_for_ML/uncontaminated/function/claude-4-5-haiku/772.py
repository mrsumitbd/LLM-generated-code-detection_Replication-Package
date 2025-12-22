import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Process command line arguments")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Model to use")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for model")
    parser.add_argument("--max_tokens", type=int, default=1024, help="Maximum tokens to generate")
    parser.add_argument("--input", type=str, help="Input file or text")
    parser.add_argument("--output", type=str, help="Output file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--api_key", type=str, help="API key for authentication")
    
    return parser.parse_args()