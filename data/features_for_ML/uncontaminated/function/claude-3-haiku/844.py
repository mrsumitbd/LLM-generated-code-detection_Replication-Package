import logging

def set_logging_level(common: CommonParameters | None = None):
    if common is None:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=common.log_level)