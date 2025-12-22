import logging

def _setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    # Force configure the root logger with a NullHandler to prevent duplicate logs
    logging.basicConfig(handlers=[logging.NullHandler()], force=True)
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        for h in logger.handlers:
            logger.removeHandler(h)

    # Check telemetry configuration to determine console logging behavior
    telemetry_config = _get_telemetry_config()

    # Only add console handlers if:
    # 1. Telemetry is not configured (default behavior)
    # 2. Telemetry debug mode is enabled
    # 3. Telemetry is disabled (fallback to console logging)
    should_log_to_console = (
        telemetry_config is None  # Telemetry not configured
        or telemetry_config.debug  # Debug mode enabled
        or not telemetry_config.enabled  # Telemetry disabled
    )

    if should_log_to_console:
        logger.addHandler(stdout_handler)
        logger.addHandler(stderr_handler)

    # Always add OpenTelemetry handler if telemetry is enabled (regardless of debug mode)
    otel_handler = _get_otel_handler()
    if otel_handler is not None:
        logger.addHandler(otel_handler)

    # Ensure the logger propagates to the root logger
    logger.propagate = True
    # Set the level on the logger itself
    logger.setLevel(level)
    return logger