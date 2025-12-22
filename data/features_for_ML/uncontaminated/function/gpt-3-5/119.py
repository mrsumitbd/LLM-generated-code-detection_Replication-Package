import sys

def flush_stdin():
    try:
        while True:
            if sys.stdin.read(1) == '':
                break
    except KeyboardInterrupt:
        pass