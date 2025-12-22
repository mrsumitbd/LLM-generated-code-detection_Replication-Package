from contextlib import contextmanager
from copy import deepcopy
from nat.runtime.loader import PluginTypes
from nat.runtime.loader import discover_and_register_plugins

class GlobalSettings:

    _global_settings: Settings | None = None

    @staticmethod
    def get() -> Settings:

        if (GlobalSettings._global_settings is None):
            from nat.runtime.loader import PluginTypes
            from nat.runtime.loader import discover_and_register_plugins

            discover_and_register_plugins(PluginTypes.REGISTRY_HANDLER)

            GlobalSettings._global_settings = Settings.from_file()

        return GlobalSettings._global_settings

    @staticmethod
    @contextmanager
    def push():

        saved = GlobalSettings.get()
        settings = deepcopy(saved)

        try:
            GlobalSettings._global_settings = settings

            yield settings
        finally:
            GlobalSettings._global_settings = saved
            GlobalSettings._global_settings._settings_changed()