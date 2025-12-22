class NotificationIcons:
    """
    通知图标常量
    """

    @classmethod
    def get(cls, reward_type: str) -> str:
        if reward_type == 'gift':
            return '🎁'
        elif reward_type == 'message':
            return '📩'
        elif reward_type == 'alert':
            return '⚠️'
        else:
            return 'ℹ️'