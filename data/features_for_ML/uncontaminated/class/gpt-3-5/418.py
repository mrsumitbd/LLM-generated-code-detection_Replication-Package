import logging
from pathlib import Path

class Logger:
    """Logger utility class for handling application logging."""

    @classmethod
    def initialize(cls, log_path: Path, log_level: str) -> None:
        logging.basicConfig(filename=log_path, level=getattr(logging, log_level.upper()))

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    @classmethod
    def set_tqdm_instance(cls, tqdm_instance) -> None:
        cls.tqdm_instance = tqdm_instance

    @staticmethod
    def log_before(retry_state: RetryCallState) -> None:
        logging.info(f"Logging before retry: {retry_state}")