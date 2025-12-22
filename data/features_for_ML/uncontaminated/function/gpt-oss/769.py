def _set_transformers_logging() -> None:
    """
    Configure the logging level for the Hugging Face Transformers library to reduce
    verbosity during normal operation. This function attempts to set the default
    verbosity to ERROR and ensures that the default handler and formatter are
    enabled. If the transformers package is not available or any error occurs,
    the function silently ignores it.
    """
    import logging

    try:
        # Try to import the transformers logging module
        from transformers import logging as hf_logging

        # Set the verbosity level to ERROR to suppress INFO/WARNING logs
        hf_logging.set_verbosity_error()

        # Ensure the default handler and formatter are enabled
        hf_logging.enable_default_handler()
        hf_logging.enable_explicit_format()
    except Exception:
        # If transformers is not installed or any other error occurs,
        # fall back to setting the standard Python logger for transformers.
        try:
            logging.getLogger("transformers").setLevel(logging.ERROR)
        except Exception:
            pass