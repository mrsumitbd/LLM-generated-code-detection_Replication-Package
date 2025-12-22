class GetLog:

    @classmethod
    def get_log(cls, log_level: str = "info", save_locally: bool = False, shared_log_folder: str = None):
        if save_locally:
            if shared_log_folder:
                print(f"Logging at {log_level} level and saving locally in {shared_log_folder}")
            else:
                print(f"Logging at {log_level} level and saving locally")
        else:
            print(f"Logging at {log_level} level")