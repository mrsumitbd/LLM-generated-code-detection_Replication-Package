def func_test_logging(app: AppInstance) -> bool:
    import logging
    import io
    
    # Create a string buffer to capture log output
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.DEBUG)
    
    # Create a logger and add the handler
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    # Test logging at different levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Get the captured output
    log_output = log_capture.getvalue()
    
    # Clean up
    logger.removeHandler(handler)
    handler.close()
    log_capture.close()
    
    # Verify that all messages were logged
    return (
        "Debug message" in log_output and
        "Info message" in log_output and
        "Warning message" in log_output and
        "Error message" in log_output
    )