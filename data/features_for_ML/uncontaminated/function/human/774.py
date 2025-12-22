import logging.handlers
import logging
import sys
from typing import Dict, Optional

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
    # Check if we already created this logger
    if name in _loggers:
        return _loggers[name]
    
    # Create the logger
    logger = logging.getLogger(name)
    
    # Only configure the logger if it hasn't been configured yet
    if not logger.handlers:
        # Set the log level
        logger.setLevel(DEFAULT_LOG_LEVEL)
        
        # Ensure log directory exists
        ensure_log_dir()
        
        # Determine which log file to use based on component
        if component is None:
            # Try to infer component from name
            if "server" in name.lower():
                log_file = SERVER_LOG_FILE
            elif "ui" in name.lower():
                log_file = UI_LOG_FILE
            elif "tts" in name.lower():
                log_file = TTS_LOG_FILE
            elif "stt" in name.lower() or "recognition" in name.lower():
                log_file = STT_LOG_FILE
            else:
                log_file = MAIN_LOG_FILE
        else:
            # Use the specified component
            log_file = COMPONENT_LOG_FILES.get(component.lower(), MAIN_LOG_FILE)
        
        # Create a rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT
        )
        
        # Create a console handler
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Create a formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set the formatter for both handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Prevent propagation to the root logger
        logger.propagate = False
    
    # Cache the logger
    _loggers[name] = logger
    
    return logger