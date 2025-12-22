def get_setting(tab: str, key: str, default: Any = None):
    import json
    import os
    from pathlib import Path
    
    config_dir = Path.home() / '.config' / 'app'
    config_file = config_dir / 'settings.json'
    
    if not config_file.exists():
        return default
    
    try:
        with open(config_file, 'r') as f:
            settings = json.load(f)
        
        if tab in settings and key in settings[tab]:
            return settings[tab][key]
        return default
    except (json.JSONDecodeError, IOError, KeyError):
        return default