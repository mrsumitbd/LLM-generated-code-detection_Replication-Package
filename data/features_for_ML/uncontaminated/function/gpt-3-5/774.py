import logging
from typing import Optional

def get_logger(name: str, component: Optional[str] = None) -> logging.Logger:
    if component is None:
        if 'server' in name:
            component = 'server'
        elif 'ui' in name:
            component = 'ui'
        elif 'tts' in name:
            component = 'tts'
        elif 'stt' in name:
            component = 'stt'
        else:
            component = 'default'
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(f'{component}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger