from os import remove, access, W_OK
from .log import logger

def rules_dir_writable() -> bool:
        """
        Checks if Prometheus rules directory is writable
        """
        try:
            with open(f"{prometheus_rules_dir}/.test.yml", "w") as f:
                f.write("Do I have a write permission?")
            remove(f"{prometheus_rules_dir}/.test.yml")
        except OSError as e:
            logger.error(
                f"The temporary file could not be created or deleted for testing permissions. {e}")
            return False
        else:
            logger.debug(
                "The application has the necessary permissions to access the rule files directory.")
            return True