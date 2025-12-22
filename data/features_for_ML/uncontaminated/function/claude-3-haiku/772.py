import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='A simple command-line argument parser.')
    parser.add_argument('--name', type=str, required=True, help='Name of the user')
    parser.add_argument('--age', type=int, required=True, help='Age of the user')
    parser.add_argument('--email', type=str, required=True, help='Email address of the user')
    args = parser.parse_args()
    return args