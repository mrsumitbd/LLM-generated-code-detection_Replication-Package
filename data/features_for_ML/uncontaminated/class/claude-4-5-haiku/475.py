class Schedule:
    """
    RemindType
        提醒类型 id	描述
        0	不提醒
        1	开始时提醒
        2	开始前 5 分钟提醒
        3	开始前 15 分钟提醒
        4	开始前 30 分钟提醒
        5	开始前 60 分钟提醒
    """
    
    REMIND_TYPES = {
        0: "不提醒",
        1: "开始时提醒",
        2: "开始前 5 分钟提醒",
        3: "开始前 15 分钟提醒",
        4: "开始前 30 分钟提醒",
        5: "开始前 60 分钟提醒"
    }
    
    REMIND_MINUTES = {
        0: 0,
        1: 0,
        2: 5,
        3: 15,
        4: 30,
        5: 60
    }
    
    def __init__(self, title="", start_time=None, end_time=None, remind_type=0, description=""):
        """
        初始化日程
        
        Args:
            title: 日程标题
            start_time: 开始时间
            end_time: 结束时间
            remind_type: 提醒类型 (0-5)
            description: 日程描述
        """
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.remind_type = remind_type if remind_type in self.REMIND_TYPES else 0
        self.description = description
    
    def get_remind_description(self):
        """获取提醒类型描述"""
        return self.REMIND_TYPES.get(self.remind_type, "不提醒")
    
    def get_remind_minutes(self):
        """获取提醒提前分钟数"""
        return self.REMIND_MINUTES.get(self.remind_type, 0)
    
    def set_remind_type(self, remind_type):
        """设置提醒类型"""
        if remind_type in self.REMIND_TYPES:
            self.remind_type = remind_type
            return True
        return False
    
    def __str__(self):
        return f"Schedule(title='{self.title}', start_time={self.start_time}, end_time={self.end_time}, remind_type={self.remind_type}, description='{self.description}')"
    
    def __repr__(self):
        return self.__str__()