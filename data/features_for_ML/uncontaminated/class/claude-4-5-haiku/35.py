import logging
import os
from datetime import datetime

class GetLog:

    @classmethod
    def get_log(cls, log_level: str = "info", save_locally: bool = False, shared_log_folder: str = None):
        logger = logging.getLogger(__name__)
        
        if logger.hasHandlers():
            return logger
        
        level = getattr(logging, log_level.upper(), logging.INFO)
        logger.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        if save_locally:
            log_dir = shared_log_folder if shared_log_folder else os.path.join(os.getcwd(), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = os.path.join(log_dir, f'log_{timestamp}.log')
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger