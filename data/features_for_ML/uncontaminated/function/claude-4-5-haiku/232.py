import signal
import sys

def signal_handler(sig, frame):
    print('\nProgram interrupted by user')
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)