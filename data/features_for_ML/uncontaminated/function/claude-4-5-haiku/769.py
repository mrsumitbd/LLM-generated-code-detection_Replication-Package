import logging
from transformers import logging as transformers_logging

def _set_transformers_logging() -> None:
    """Set up logging for transformers library."""
    transformers_logging.set_verbosity_error()
    logging.getLogger("transformers").setLevel(logging.ERROR)