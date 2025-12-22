import logging

class LogContext:
    def __init__(self, **kwargs):
        self.log_level = kwargs.get('log_level', logging.INFO)
        self.log_format = kwargs.get('log_format', '%(asctime)s - %(levelname)s - %(message)s')
        self.log_file = kwargs.get('log_file', None)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)
        formatter = logging.Formatter(self.log_format)

        if self.log_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        else:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

    def __enter__(self):
        return self.logger

    def __exit__(self, exc_type, exc_value, traceback):
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)