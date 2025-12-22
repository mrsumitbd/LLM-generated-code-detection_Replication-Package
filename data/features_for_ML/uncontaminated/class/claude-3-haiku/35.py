import logging
import os

class GetLog:

    @classmethod
    def get_log(cls, log_level: str = "info", save_locally: bool = False, shared_log_folder: str = None):
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, log_level.upper()))

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        if save_locally:
            if shared_log_folder:
                log_file = os.path.join(shared_log_folder, f"{__name__}.log")
            else:
                log_file = f"{__name__}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger