import logging
import logging.config

def config_loggers(in_logger_config: LoggerConfigData):
    logging.config.dictConfig(in_logger_config.to_dict())