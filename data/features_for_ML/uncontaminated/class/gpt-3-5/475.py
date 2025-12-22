class Schedule:
    def __init__(self, event_name, event_time, remind_type=0):
        self.event_name = event_name
        self.event_time = event_time
        self.remind_type = remind_type

    def set_remind_type(self, remind_type):
        self.remind_type = remind_type

    def get_remind_type(self):
        return self.remind_type

    def get_event_details(self):
        return f"Event: {self.event_name}, Time: {self.event_time}, Remind Type: {self.remind_type}"