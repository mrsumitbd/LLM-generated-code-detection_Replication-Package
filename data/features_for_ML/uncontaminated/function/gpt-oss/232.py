import sys

def signal_handler(sig, frame):
    """Handle interrupt signals (e.g., SIGINT)."""
    print("\nInterrupt received, exiting gracefully.")
    sys.exit(0)