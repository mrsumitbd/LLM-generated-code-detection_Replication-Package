import logging
from pathlib import Path
from typing import Optional

from tenacity import RetryCallState


class Logger:
    """Logger utility class for handling application logging."""

    _tqdm_instance: Optional[object] = None

    @classmethod
    def initialize(cls, log_path: Path, log_level: str) -> None:
        """
        Configure the root logger.

        Parameters
        ----------
        log_path : Path
            Path to the log file.
        log_level : str
            Logging level as a string (e.g., 'DEBUG', 'INFO').
        """
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            handlers=[
                logging.FileHandler(log_path, mode="a", encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
        # Ensure root logger uses the same level
        logging.getLogger().setLevel(numeric_level)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Retrieve a named logger.

        Parameters
        ----------
        name : str
            Name of the logger.

        Returns
        -------
        logging.Logger
            The logger instance.
        """
        return logging.getLogger(name)

    @classmethod
    def set_tqdm_instance(cls, tqdm_instance) -> None:
        """
        Store a tqdm instance for use in log messages.

        Parameters
        ----------
        tqdm_instance : object
            An instance of tqdm (or compatible) that provides a `write` method.
        """
        cls._tqdm_instance = tqdm_instance

    @staticmethod
    def log_before(retry_state: RetryCallState) -> None:
        """
        Log a message before a retry attempt.

        Parameters
        ----------
        retry_state : RetryCallState
            The state object provided by tenacity.
        """
        attempt = retry_state.attempt_number
        exception = retry_state.outcome.exception()
        msg = f"Retry attempt {attempt} after exception: {exception!r}"
        logger = logging.getLogger(retry_state.fn.__module__)
        if Logger._tqdm_instance is not None:
            # If tqdm is available, write to it instead of the console
            try:
                Logger._tqdm_instance.write(msg)
            except Exception:
                logger.warning(msg)
        else:
            logger.warning(msg)