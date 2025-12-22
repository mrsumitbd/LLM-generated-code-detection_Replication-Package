import logging
from pathlib import Path
from typing import Optional
from tenacity import RetryCallState
import tqdm as tqdm_module

class Logger:
    """Logger utility class for handling application logging."""

    _loggers: dict = {}
    _log_path: Optional[Path] = None
    _log_level: str = "INFO"
    _tqdm_instance: Optional[tqdm_module.tqdm] = None

    @classmethod
    def initialize(cls, log_path: Path, log_level: str) -> None:
        cls._log_path = log_path
        cls._log_level = log_level.upper()
        
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, cls._log_level))
        
        if root_logger.handlers:
            root_logger.handlers.clear()
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, cls._log_level))
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, cls._log_level))
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        return logger

    @classmethod
    def set_tqdm_instance(cls, tqdm_instance) -> None:
        cls._tqdm_instance = tqdm_instance

    @staticmethod
    def log_before(retry_state: RetryCallState) -> None:
        logger = logging.getLogger(__name__)
        attempt_number = retry_state.attempt_number
        logger.warning(
            f"Retry attempt {attempt_number} for {retry_state.fn.__name__}"
        )