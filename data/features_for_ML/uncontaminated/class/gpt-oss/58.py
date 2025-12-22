class AstraYaoQuickAssistManagerTriggerRecord:
    def __init__(self, trigger_id=None, trigger_name=None, trigger_time=None, trigger_data=None):
        self.trigger_id = trigger_id
        self.trigger_name = trigger_name
        self.trigger_time = trigger_time
        self.trigger_data = trigger_data

    def to_dict(self):
        return {
            "trigger_id": self.trigger_id,
            "trigger_name": self.trigger_name,
            "trigger_time": self.trigger_time,
            "trigger_data": self.trigger_data,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_id=data.get("trigger_id"),
            trigger_name=data.get("trigger_name"),
            trigger_time=data.get("trigger_time"),
            trigger_data=data.get("trigger_data"),
        )

    def __repr__(self):
        return f"AstraYaoQuickAssistManagerTriggerRecord({self.to_dict()})"

    def __eq__(self, other):
        if not isinstance(other, AstraYaoQuickAssistManagerTriggerRecord):
            return False
        return self.to_dict() == other.to_dict()

    def __hash__(self):
        return hash((
            self.trigger_id,
            self.trigger_name,
            self.trigger_time,
            self.trigger_data,
        ))