import logging
from pathlib import Path
from typing import Optional

from retry.api import RetryCallState
from tqdm import tqdm

class Logger:
    """Logger utility class for handling application logging."""

    _logger: Optional[logging.Logger] = None
    _tqdm_instance: Optional[tqdm] = None

    @classmethod
    def initialize(cls, log_path: Path, log_level: str) -> None:
        logging.basicConfig(
            filename=str(log_path),
            level=getattr(logging, log_level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        cls._logger = logging.getLogger(__name__)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    @classmethod
    def set_tqdm_instance(cls, tqdm_instance) -> None:
        cls._tqdm_instance = tqdm_instance

    @staticmethod
    def log_before(retry_state: RetryCallState) -> None:
        if Logger._tqdm_instance:
            Logger._tqdm_instance.write(
                f"Retrying function {retry_state.func_name!r} "
                f"(call {retry_state.attempt_number} of {retry_state.max_attempts})"
            )
        Logger.get_logger(__name__).info(
            f"Retrying function {retry_state.func_name!r} "
            f"(call {retry_state.attempt_number} of {retry_state.max_attempts})"
        )