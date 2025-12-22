def get_setting(tab: str, key: str, default: Any = None):
    settings = {
        'general': {
            'theme': 'light',
            'language': 'english'
        },
        'advanced': {
            'auto_save': True,
            'show_warnings': True
        }
    }
    
    return settings.get(tab, {}).get(key, default)