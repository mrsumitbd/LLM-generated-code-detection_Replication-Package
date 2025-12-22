import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional

# Define the directory where log files will be stored
_LOG_DIR = Path(__file__).parent / "logs"
_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Default component if none can be inferred
_DEFAULT_COMPONENT = "general"

# Known component keywords for inference
_COMPONENT_KEYWORDS = {
    "server": ["server", "srv"],
    "ui": ["ui", "frontend", "gui"],
    "tts": ["tts", "texttospeech"],
    "stt": ["stt", "speechrecognition", "speech_to_text"],
}

def _infer_component(name: str) -> str:
    """Infer component name from the logger name."""
    lower = name.lower()
    for comp, keywords in _COMPONENT_KEYWORDS.items():
        if any(k in lower for k in keywords):
            return comp
    return _DEFAULT_COMPONENT

def get_logger(name: str, component: Optional[str] = None) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: The name of the logger, typically __name__ of the calling module
        component: Optional component name to determine log file (server, ui, tts, stt)
                   If None, it will be inferred from the name

    Returns:
        A configured logger instance
    """
    # Resolve component
    if component is None:
        component = _infer_component(name)

    logger = logging.getLogger(name)
    # Avoid reconfiguring if already configured
    if getattr(logger, "_configured", False):
        return logger

    logger.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_file = _LOG_DIR / f"{component}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Mark as configured to avoid duplicate handlers
    logger._configured = True
    return logger