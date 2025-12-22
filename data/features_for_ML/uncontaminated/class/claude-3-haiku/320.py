import threading

class Settings:
    def __init__(self):
        self.debug_mode = False
        self.log_level = 'info'
        self.api_key = None

class GlobalSettings:
    _local = threading.local()

    @staticmethod
    def get() -> Settings:
        if hasattr(GlobalSettings._local, 'settings'):
            return GlobalSettings._local.settings
        else:
            GlobalSettings._local.settings = Settings()
            return GlobalSettings._local.settings

    @staticmethod
    @contextmanager
    def push():
        old_settings = GlobalSettings.get()
        new_settings = Settings()
        new_settings.__dict__.update(old_settings.__dict__)
        GlobalSettings._local.settings = new_settings
        try:
            yield new_settings
        finally:
            GlobalSettings._local.settings = old_settings