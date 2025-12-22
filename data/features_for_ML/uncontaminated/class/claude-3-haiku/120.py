class VivianDotTriggerRecord:
    def __init__(self):
        self.trigger_id = None
        self.trigger_name = None
        self.trigger_type = None
        self.trigger_condition = None
        self.trigger_action = None
        self.trigger_status = None
        self.trigger_created_at = None
        self.trigger_updated_at = None

    def set_trigger_id(self, trigger_id):
        self.trigger_id = trigger_id

    def get_trigger_id(self):
        return self.trigger_id

    def set_trigger_name(self, trigger_name):
        self.trigger_name = trigger_name

    def get_trigger_name(self):
        return self.trigger_name

    def set_trigger_type(self, trigger_type):
        self.trigger_type = trigger_type

    def get_trigger_type(self):
        return self.trigger_type

    def set_trigger_condition(self, trigger_condition):
        self.trigger_condition = trigger_condition

    def get_trigger_condition(self):
        return self.trigger_condition

    def set_trigger_action(self, trigger_action):
        self.trigger_action = trigger_action

    def get_trigger_action(self):
        return self.trigger_action

    def set_trigger_status(self, trigger_status):
        self.trigger_status = trigger_status

    def get_trigger_status(self):
        return self.trigger_status

    def set_trigger_created_at(self, trigger_created_at):
        self.trigger_created_at = trigger_created_at

    def get_trigger_created_at(self):
        return self.trigger_created_at

    def set_trigger_updated_at(self, trigger_updated_at):
        self.trigger_updated_at = trigger_updated_at

    def get_trigger_updated_at(self):
        return self.trigger_updated_at