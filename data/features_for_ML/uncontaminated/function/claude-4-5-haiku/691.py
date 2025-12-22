def graceful_signal_handler(signum, frame):
    """
    Custom signal handler to gracefully handle SIGTERM when Locust is already shutting down.
    This prevents the "stopping state" exception from being raised.
    """
    import sys
    sys.exit(0)