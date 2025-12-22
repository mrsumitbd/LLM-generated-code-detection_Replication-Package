def unexpect_error(context: str = None, error: Exception = None):
    import logging
    import traceback

    log_message = f"Unexpected error occurred in the context: {context}" if context else "Unexpected error occurred"
    log_message += f"\nError: {error}" if error else ""
    log_message += f"\nTraceback: {traceback.format_exc()}"

    logging.error(log_message)