def set_logging_level(common: CommonParameters | None = None):
    import logging
    
    if common is None:
        logging.basicConfig(level=logging.WARNING)
        return
    
    log_level = getattr(common, 'log_level', None)
    
    if log_level is None:
        logging.basicConfig(level=logging.WARNING)
        return
    
    level_map = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    
    if isinstance(log_level, str):
        level = level_map.get(log_level.lower(), logging.WARNING)
    elif isinstance(log_level, int):
        level = log_level
    else:
        level = logging.WARNING
    
    logging.basicConfig(level=level)