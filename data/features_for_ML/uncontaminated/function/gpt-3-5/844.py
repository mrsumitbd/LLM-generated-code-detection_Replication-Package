def set_logging_level(common: CommonParameters | None = None):
    if common is None:
        # Default logging level
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=common.logging_level)