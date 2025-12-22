def graceful_signal_handler(signum, frame):
    """
    Custom signal handler to gracefully handle SIGTERM when Locust is already shutting down.
    This prevents the "stopping state" exception from being raised.
    """
    try:
        from locust.runners import locust_runner
        if locust_runner and locust_runner.state == "stopping":
            print("Received SIGTERM while Locust is already shutting down, exiting gracefully.")
            sys.exit(0)
    except ImportError:
        pass