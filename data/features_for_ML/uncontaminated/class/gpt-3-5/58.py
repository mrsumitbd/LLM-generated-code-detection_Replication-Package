class AstraYaoQuickAssistManagerTriggerRecord:
    
    def __init__(self):
        self.trigger_id = None
        self.trigger_name = None
        self.trigger_type = None
        self.trigger_time = None
        self.trigger_status = None

    def set_trigger_id(self, trigger_id):
        self.trigger_id = trigger_id

    def set_trigger_name(self, trigger_name):
        self.trigger_name = trigger_name

    def set_trigger_type(self, trigger_type):
        self.trigger_type = trigger_type

    def set_trigger_time(self, trigger_time):
        self.trigger_time = trigger_time

    def set_trigger_status(self, trigger_status):
        self.trigger_status = trigger_status

    def get_trigger_id(self):
        return self.trigger_id

    def get_trigger_name(self):
        return self.trigger_name

    def get_trigger_type(self):
        return self.trigger_type

    def get_trigger_time(self):
        return self.trigger_time

    def get_trigger_status(self):
        return self.trigger_status