def func_test_logging(app: AppInstance) -> bool:
    try:
        app.logger.info("Testing logging functionality...")
        app.logger.debug("This is a debug message.")
        app.logger.warning("This is a warning message.")
        app.logger.error("This is an error message.")
        app.logger.critical("This is a critical message.")
        return True
    except Exception as e:
        app.logger.error(f"Error occurred while testing logging: {str(e)}")
        return False