class YuzuhaCinema4QuickAssistTriggerRecord:

    def __init__(self):
        self.trigger_record = []

    def add_trigger(self, trigger_name, trigger_time):
        self.trigger_record.append((trigger_name, trigger_time))

    def get_trigger_record(self):
        return self.trigger_record

# Example usage:
# cinema_record = YuzuhaCinema4QuickAssistTriggerRecord()
# cinema_record.add_trigger("Scene1", "00:05:30")
# cinema_record.add_trigger("Scene2", "00:10:15")
# print(cinema_record.get_trigger_record())