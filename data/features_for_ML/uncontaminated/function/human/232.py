import sys

def signal_handler(sig, frame):
        logger.info(f"Received signal: {sig}")
        if cleanup_func:
            cleanup_func()
        sys.exit(0)