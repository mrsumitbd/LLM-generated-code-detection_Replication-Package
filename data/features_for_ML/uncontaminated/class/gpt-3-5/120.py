class VivianDotTriggerRecord:
    
    def __init__(self):
        self.triggered = False
        self.record = None

    def set_triggered(self, value):
        self.triggered = value

    def set_record(self, record):
        self.record = record

    def get_triggered(self):
        return self.triggered

    def get_record(self):
        return self.record