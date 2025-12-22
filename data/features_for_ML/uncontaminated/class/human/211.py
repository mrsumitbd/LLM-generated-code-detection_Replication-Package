
class NotificationIcons:
    """
    通知图标常量
    """
    UPLOAD = "⬆️"
    DOWNLOAD = "⬇️"
    BONUS = "✨"
    WORK = "🔧"
    POWER = "⚡"
    VICOMO = "🐘"
    FROG = "🐸"
    VIP = "👑"
    RAINBOW = "🌈"
    FEEDBACK = "📝"
    DEFAULT = "📌"
    
    @classmethod
    def get(cls, reward_type: str) -> str:
        """
        获取奖励类型对应的图标
        """
        icon_map = {
            "上传量": cls.UPLOAD,
            "下载量": cls.DOWNLOAD,
            "魔力值": cls.BONUS,
            "工分": cls.WORK,
            "电力": cls.POWER,
            "象草": cls.VICOMO,
            "青蛙": cls.FROG,
            "VIP": cls.VIP,
            "彩虹ID": cls.RAINBOW,
            "raw_feedback": cls.FEEDBACK
        }
        return icon_map.get(reward_type, cls.DEFAULT)