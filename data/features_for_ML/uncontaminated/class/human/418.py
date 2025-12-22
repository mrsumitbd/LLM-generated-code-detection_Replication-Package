import logging
import sys
from pathlib import Path
from tenacity import RetryCallState

class Logger:
    """Logger utility class for handling application logging."""

    _initialized = False
    _tqdm_handler: TqdmCompatibleHandler | None = None

    @classmethod
    def initialize(cls, log_path: Path, log_level: str) -> None:
        """
        Initialize the logger with specified path and level.

        Args:
            log_path: Path to the log file
            log_level: Logging level as string (e.g., "INFO", "DEBUG")
        """
        if cls._initialized:
            return

        # Parse log level
        level = getattr(logging, log_level.upper(), logging.INFO)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create tqdm-compatible console handler
        cls._tqdm_handler = TqdmCompatibleHandler(sys.stdout)

        handlers = [
            logging.FileHandler(log_path, encoding="utf-8"),
            cls._tqdm_handler,
        ]
        fmt = (
            "%(asctime)s [%(levelname)s] "
            "%(filename)s:%(lineno)d "
            "[%(funcName)s] %(message)s"
        )
        logging.basicConfig(level=level, format=fmt, handlers=handlers)
        cls._initialized = True

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance with the specified name.

        Args:
            name: Name of the logger

        Returns:
            Logger instance
        """
        return logging.getLogger(name)

    @classmethod
    def set_tqdm_instance(cls, tqdm_instance) -> None:
        """
        Set the tqdm instance for coordinated logging.

        Args:
            tqdm_instance: The tqdm progress bar instance
        """
        if cls._tqdm_handler:
            cls._tqdm_handler.set_tqdm(tqdm_instance)

    @staticmethod
    def log_before(retry_state: RetryCallState) -> None:
        """
        Log information before a retry attempt.

        Args:
            retry_state: Retry call state information
        """
        attempt = retry_state.attempt_number
        if attempt > 1:
            logger = Logger.get_logger("retry")
            fn = retry_state.fn
            exc = retry_state.outcome.exception() if retry_state.outcome else None
            logger.warning(f"Retrying {fn.__name__} (attempt {attempt})... Reason: {exc}")