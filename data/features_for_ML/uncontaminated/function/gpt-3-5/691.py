def graceful_signal_handler(signum, frame):
    import signal
    import locust
    
    if signum == signal.SIGTERM and locust.runners.locust_runner is not None:
        locust.runners.locust_runner.quit()