import requests
from scenarios.base import AppInstance, Scenario

def func_test_logging(app: AppInstance) -> bool:
    port, logger = app.port, app.logger
    test_messages = ["This is a log message", "This is another log message"]

    for message in test_messages:
        # Post Messages
        url_log = f"http://localhost:{port}/log"
        r = requests.post(url=url_log, json={"message": message})
        if not r.ok:
            logger.warning(f"Failed to log message: {message}")
            return False

        logger.info(f"got 200 response: {message}")

        # Get Messages
        url_logs = f"http://localhost:{port}/logs"
        requested_logs = requests.get(url=url_logs)
        if not requested_logs.ok:
            logger.warning("Failed to retrieve logs from server")
            return False

        logs = requested_logs.text.splitlines()
        if logs[-1] != message:
            logger.warning(f"Failed to log message: {message}")
            return False

    return True