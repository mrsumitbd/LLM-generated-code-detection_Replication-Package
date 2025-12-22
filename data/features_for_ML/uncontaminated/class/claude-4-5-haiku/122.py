class LogContext:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.original_state = {}

    def __enter__(self):
        import logging
        
        for key, value in self.kwargs.items():
            if key == 'level':
                logger = logging.getLogger()
                self.original_state['level'] = logger.level
                logger.setLevel(value)
            elif key == 'format':
                logger = logging.getLogger()
                for handler in logger.handlers:
                    formatter = logging.Formatter(value)
                    self.original_state[f'formatter_{id(handler)}'] = handler.formatter
                    handler.setFormatter(formatter)
            elif key == 'logger':
                logger = logging.getLogger(value)
                self.original_state['logger'] = logger
        
        return self

    def __exit__(self, *args):
        import logging
        
        if 'level' in self.original_state:
            logger = logging.getLogger()
            logger.setLevel(self.original_state['level'])
        
        for key, value in self.original_state.items():
            if key.startswith('formatter_'):
                handler_id = int(key.split('_')[1])
                logger = logging.getLogger()
                for handler in logger.handlers:
                    if id(handler) == handler_id:
                        handler.setFormatter(value)
                        break