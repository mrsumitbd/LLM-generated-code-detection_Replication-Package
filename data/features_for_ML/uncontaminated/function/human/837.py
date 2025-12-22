from primary.config import API_KEY, API_URL, API_TIMEOUT, COMMAND_WAIT_DELAY, COMMAND_WAIT_ATTEMPTS, APP_TYPE
import time
from primary.utils.logger import logger, debug_log

def wait_for_command(command_id: int):
    logger.debug(f"Waiting for command {command_id} to complete...")
    attempts = 0
    while True:
        try:
            time.sleep(COMMAND_WAIT_DELAY)
            response = arr_request(f"command/{command_id}")
            logger.debug(f"Command {command_id} Status: {response['status']}")
        except Exception as error:
            logger.error(f"Error fetching command status on attempt {attempts + 1}: {error}")
            return False

        attempts += 1

        if response['status'].lower() in ['complete', 'completed'] or attempts >= COMMAND_WAIT_ATTEMPTS:
            break

    if response['status'].lower() not in ['complete', 'completed']:
        logger.warning(f"Command {command_id} did not complete within the allowed attempts.")
        return False

    time.sleep(0.5)

    return response['status'].lower() in ['complete', 'completed']