import logging

def set_logging_level(common: CommonParameters | None = None):
    if common and common.quiet:
        level = logging.ERROR
    elif common and common.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    __setup_logging(level)