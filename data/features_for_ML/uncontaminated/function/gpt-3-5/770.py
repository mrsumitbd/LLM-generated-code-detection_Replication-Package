import logging
from logging.config import dictConfig

def get_logger(name: str) -> logging.Logger:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "rich": {
                "()": "rich.logging.RichHandler",
                "formatter": "rich",
                "level": "INFO",
                "show_path": False,
                "show_time": True,
            },
            "json": {
                "()": "rich.logging.RichHandler",
                "formatter": "json",
                "level": "INFO",
                "show_path": False,
                "show_time": True,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "rich",
                "level": "INFO",
            },
            "json_console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "level": "INFO",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "INFO",
            },
            "json": {
                "handlers": ["json_console"],
                "level": "INFO",
            },
        },
    }

    dictConfig(logging_config)
    return logging.getLogger(name)