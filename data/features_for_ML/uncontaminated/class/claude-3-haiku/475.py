from datetime import datetime, timedelta

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

    def __init__(self, start_time: datetime, end_time: datetime, remind_type: int = 0):
        self.start_time = start_time
        self.end_time = end_time
        self.remind_type = remind_type

    def get_remind_time(self) -> datetime:
        if self.remind_type == 0:
            return None
        elif self.remind_type == 1:
            return self.start_time
        elif self.remind_type == 2:
            return self.start_time - timedelta(minutes=5)
        elif self.remind_type == 3:
            return self.start_time - timedelta(minutes=15)
        elif self.remind_type == 4:
            return self.start_time - timedelta(minutes=30)
        elif self.remind_type == 5:
            return self.start_time - timedelta(minutes=60)
        else:
            raise ValueError("Invalid remind_type value")

    def get_duration(self) -> timedelta:
        return self.end_time - self.start_time

    def __str__(self):
        return f"Schedule(start_time={self.start_time}, end_time={self.end_time}, remind_type={self.remind_type})"