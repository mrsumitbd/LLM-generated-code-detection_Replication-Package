import logging

def _setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    # Force configure the root logger with a NullHandler to prevent duplicate logs
    logging.getLogger().addHandler(logging.NullHandler())

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger