import logging

class LogContext:

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info("Log context initialized with kwargs: %s", kwargs)

    def __enter__(self):
        self.logger.info("Entering log context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.logger.error("An exception occurred: %s", exc_val)
        self.logger.info("Exiting log context")

# Example usage:
# with LogContext(user="Alice", action="login") as log:
#     log.logger.info("User %s logged in", log.user)