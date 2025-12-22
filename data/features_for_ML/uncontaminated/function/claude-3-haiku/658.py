def get_setting(tab: str, key: str, default: Any = None):
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        if tab in config.sections():
            if key in config[tab]:
                return config[tab][key]
    except (ImportError, FileNotFoundError, KeyError):
        pass
    return default