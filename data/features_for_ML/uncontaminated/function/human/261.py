def check_and_notify():
    """Check for updates and notify user if available.

    This is the main entry point for version checking.
    """
    try:
        result = check_for_updates()
        if result:
            latest_version, update_available = result
            if update_available:
                prompt_for_update(latest_version)
    except Exception as e:
        # Never let version checking break the main program
        logger.debug(f"Version check failed: {e}")
        pass