class NotificationIcons:
    """
    通知图标常量
    """

    _ICONS = {
        "gold": "🏅",
        "silver": "🥈",
        "bronze": "🥉",
        "diamond": "💎",
        "gift": "🎁",
        "achievement": "🏆",
        "level_up": "📈",
        "friend_request": "👥",
        "message": "✉️",
    }

    @classmethod
    def get(cls, reward_type: str) -> str:
        """
        根据奖励类型返回对应的通知图标。

        :param reward_type: 奖励类型字符串
        :return: 对应的图标字符串
        """
        if not isinstance(reward_type, str):
            return "🔔"
        key = reward_type.lower()
        return cls._ICONS.get(key, "🔔")