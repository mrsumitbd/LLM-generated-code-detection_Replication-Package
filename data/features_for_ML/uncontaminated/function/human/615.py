from agno.utils.log import logger
import os

def handle_exit(sig, frame):
        logger.info(
            "Received shutdown signal - exiting immediately without waiting for connections"
        )
        os._exit(0)