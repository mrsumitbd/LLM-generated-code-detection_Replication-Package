import sys

def flush_stdin():
    try:
        while True:
            char = sys.stdin.read(1)
            if not char:
                break
    except IOError:
        pass