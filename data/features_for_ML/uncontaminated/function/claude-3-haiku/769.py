import logging
from transformers import logging as transformers_logging

def _set_transformers_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    transformers_logging.set_verbosity_info()
    transformers_logging.enable_default_handler()
    transformers_logging.enable_explicit_format()