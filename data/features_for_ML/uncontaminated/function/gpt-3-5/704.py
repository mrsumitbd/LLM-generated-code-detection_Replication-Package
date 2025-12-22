def func_test_logging(app: AppInstance) -> bool:
    try:
        app.logger.debug("Testing logging")
        return True
    except Exception as e:
        print(f"Error testing logging: {e}")
        return False