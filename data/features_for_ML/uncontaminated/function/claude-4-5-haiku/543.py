def _get_push_channels() -> list[str]:
    import os
    
    channels = os.environ.get('PUSH_CHANNELS', '').split(',')
    return [ch.strip() for ch in channels if ch.strip()]