import logging
import logging.config
from typing import Any, Dict

def config_loggers(in_logger_config: LoggerConfigData):
    """Configure loggers based on LoggerConfigData."""
    config_dict: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {},
        'handlers': {},
        'loggers': {},
        'root': {}
    }
    
    # Configure formatters
    if hasattr(in_logger_config, 'formatters') and in_logger_config.formatters:
        for formatter_name, formatter_config in in_logger_config.formatters.items():
            config_dict['formatters'][formatter_name] = {
                'format': formatter_config.get('format', '%(message)s'),
                'datefmt': formatter_config.get('datefmt')
            }
    
    # Configure handlers
    if hasattr(in_logger_config, 'handlers') and in_logger_config.handlers:
        for handler_name, handler_config in in_logger_config.handlers.items():
            handler_dict = {
                'class': handler_config.get('class', 'logging.StreamHandler'),
                'level': handler_config.get('level', 'NOTSET'),
                'formatter': handler_config.get('formatter', 'default')
            }
            if 'filename' in handler_config:
                handler_dict['filename'] = handler_config['filename']
            config_dict['handlers'][handler_name] = handler_dict
    
    # Configure loggers
    if hasattr(in_logger_config, 'loggers') and in_logger_config.loggers:
        for logger_name, logger_config in in_logger_config.loggers.items():
            config_dict['loggers'][logger_name] = {
                'level': logger_config.get('level', 'NOTSET'),
                'handlers': logger_config.get('handlers', []),
                'propagate': logger_config.get('propagate', True)
            }
    
    # Configure root logger
    if hasattr(in_logger_config, 'root'):
        root_config = in_logger_config.root
        config_dict['root'] = {
            'level': root_config.get('level', 'WARNING'),
            'handlers': root_config.get('handlers', [])
        }
    
    logging.config.dictConfig(config_dict)