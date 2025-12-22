class NotificationIcons:
    """
    通知图标常量
    """

    REWARD_TYPE_GOLD = "gold"
    REWARD_TYPE_SILVER = "silver"
    REWARD_TYPE_BRONZE = "bronze"

    ICON_MAP = {
        REWARD_TYPE_GOLD: "🏆",
        REWARD_TYPE_SILVER: "🥈",
        REWARD_TYPE_BRONZE: "🥉",
    }

    @classmethod
    def get(cls, reward_type: str) -> str:
        if reward_type not in cls.ICON_MAP:
            raise ValueError(f"Invalid reward type: {reward_type}")
        return cls.ICON_MAP[reward_type]