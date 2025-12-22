import logging
from typing import List

class LoggerConfigData:
    def __init__(self, loggers: List[str], log_level: int):
        self.loggers = loggers
        self.log_level = log_level

def config_loggers(in_logger_config: LoggerConfigData):
    logging.basicConfig(level=in_logger_config.log_level)
    for logger_name in in_logger_config.loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(in_logger_config.log_level)