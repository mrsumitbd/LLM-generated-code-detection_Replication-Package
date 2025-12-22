class AstraYaoChordManagerTriggerRecord:
    def __init__(self):
        self.trigger_id = None
        self.trigger_type = None
        self.trigger_value = None
        self.trigger_time = None
        self.trigger_status = None
        self.trigger_message = None

    def set_trigger_id(self, trigger_id):
        self.trigger_id = trigger_id

    def set_trigger_type(self, trigger_type):
        self.trigger_type = trigger_type

    def set_trigger_value(self, trigger_value):
        self.trigger_value = trigger_value

    def set_trigger_time(self, trigger_time):
        self.trigger_time = trigger_time

    def set_trigger_status(self, trigger_status):
        self.trigger_status = trigger_status

    def set_trigger_message(self, trigger_message):
        self.trigger_message = trigger_message

    def get_trigger_id(self):
        return self.trigger_id

    def get_trigger_type(self):
        return self.trigger_type

    def get_trigger_value(self):
        return self.trigger_value

    def get_trigger_time(self):
        return self.trigger_time

    def get_trigger_status(self):
        return self.trigger_status

    def get_trigger_message(self):
        return self.trigger_message