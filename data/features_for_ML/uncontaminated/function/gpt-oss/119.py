import sys
import select
import os

def flush_stdin():
    """
    Flush any pending data from sys.stdin without blocking.
    """
    # Use non-blocking select to check for available input
    while True:
        rlist, _, _ = select.select([sys.stdin], [], [], 0)
        if not rlist:
            break
        try:
            # Read a chunk of data; discard it
            data = os.read(sys.stdin.fileno(), 1024)
            if not data:
                break
        except OSError:
            break