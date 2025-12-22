def close_loggers(loggers: List[logging.Logger]) -> None:
    for logger in loggers:
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)