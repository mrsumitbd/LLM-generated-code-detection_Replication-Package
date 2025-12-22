class NotificationIcons:
    """
    通知图标常量
    """
    
    _ICONS = {
        'coin': '💰',
        'gem': '💎',
        'exp': '⭐',
        'item': '📦',
        'achievement': '🏆',
        'level_up': '📈',
        'bonus': '🎁',
        'warning': '⚠️',
        'error': '❌',
        'success': '✅',
        'info': 'ℹ️',
        'default': '📢'
    }

    @classmethod
    def get(cls, reward_type: str) -> str:
        return cls._ICONS.get(reward_type.lower(), cls._ICONS['default'])